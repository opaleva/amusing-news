import json

from django.contrib.contenttypes.models import ContentType
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

from comments.models import Comment
from articles.models import Article

logger = logging.getLogger(__name__)


class CommentsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        logger.error('Connection')
        self.article_id = self.scope['url_route']['kwargs']['article_id']
        self.article_group_name = 'article_%s' % self.article_id

        await self.channel_layer.group_add(
            self.article_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        logger.warning('Disconnection')
        await self.channel_layer.group_discard(
            self.article_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        comment = text_data_json['text']
        new_comment = await self.create_new(comment)
        data = {
            'author': new_comment.author.username,
            'created': new_comment.created.strftime('%Y-%m-%d %H:%m'),
            'text': new_comment.text
        }

        await self.channel_layer.group_send(
            self.article_group_name,
            {
                'type': 'new_comment',
                'message': data
            }
        )

    async def new_comment(self, event):
        message = event['message']

        await self.send(
            text_data=json.dumps({
                'message': message
            })
        )

    @database_sync_to_async
    def create_new(self, text):
        ct = ContentType.objects.get_for_model(Article)
        new_comment = Comment.objects.create(
            author=self.scope['user'],
            text=text,
            content_type=ct,
            object_id=int(self.article_id)
        )
        return new_comment
