# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Post
from django.contrib import admin


class adminPost(admin.ModelAdmin):
    list_display = ["title","category","timestamp","updated"]
    list_display_links = ["title"]
    list_filter = ["category"]
    search_fields = ["title","category"]

    class Meta:
        model = Post

# Register your models here.
admin.site.register(Post,adminPost)