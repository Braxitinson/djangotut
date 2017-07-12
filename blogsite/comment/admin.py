# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from comment.models import Comment
# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ["user","id","object_id","timestamp","content_object"]

    class Meta:
        model = Comment


admin.site.register(Comment,CommentAdmin)