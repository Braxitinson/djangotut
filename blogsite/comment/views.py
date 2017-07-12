# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType


from django.shortcuts import render
from comment.models import Comment
from comment.forms import CommentForm

# Create your views here.
def comment_detail(request, id=None):
    instance = get_object_or_404(Comment, id=id)

    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.object_id,
    }

    comment_forms = CommentForm(request.POST or None, initial=initial_data)
    if comment_forms.is_valid():
        c_type = comment_forms.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = comment_forms.cleaned_data.get('object_id')
        content_data = comment_forms.cleaned_data.get('content')
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    context = {
        "instance": instance,
        "comment_form": comment_forms,
    }


    return render(request, 'comment_detail.html', context)
