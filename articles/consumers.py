import json
import locale

from django.contrib.contenttypes.models import ContentType
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

from comments.models import Comment
from articles.models import Article

logger = logging.getLogger(__name__)


class CommentsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        logger.debug('Connection')
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
        locale.setlocale(locale.LC_TIME, "de_DE.utf8")
        data = {
            'author': new_comment.author.username,
            'city': new_comment.author.city,
            'created': new_comment.created.strftime('%-d. %B %Y %H:%M'),
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
        if not message:
            logger.error('Failed to leave a comment')
        else:
            logger.debug('Comment added successfully')
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
