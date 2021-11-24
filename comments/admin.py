from django.contrib import admin

from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('author', 'text')
