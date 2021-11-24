from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import View

import logging

from .forms import CommentForm

logger = logging.getLogger(__name__)


class CommentCreateView(View):

    @staticmethod
    def post(request, *args, **kwargs):
        form = CommentForm(request.POST or None)
        ct = ContentType.objects.get(model=kwargs['content_type'])
        model = ct.model_class().objects.get(pk=kwargs['object_id'])
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.text = form.cleaned_data['text']
            new_comment.content_object = model
            new_comment.save()
            if new_comment is None:
                logger.error("Problem with posting a comment")
            return HttpResponseRedirect(model.get_absolute_url())
        messages.add_message(request, messages.ERROR, logger.error('Failed to leave a comment'))
        return HttpResponseRedirect(model.get_absolute_url())
