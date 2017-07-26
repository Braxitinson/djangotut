# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.contenttypes.models import ContentType


from django.shortcuts import render
from comment.models import Comment
from comment.forms import CommentForm

# Create your views here.
def comment_thread(request, id=None):
    # instance = get_object_or_404(Comment, id=id)
    try:
        instance = Comment.objects.get(id=id)
    except:
        raise Http404


    initial_data = {
        "content_type": instance.content_object.get_content_type,
        "object_id": instance.object_id,
    }

    comment_forms = CommentForm(request.POST or None, initial=initial_data)
    print(comment_forms.errors)

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
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "instance": instance,
        "comment_forms": comment_forms,
    }


    return render(request, 'comment_thread.html', context)

@login_required(login_url='/login/')
def comment_delete(request, id):
    # obj = get_object_or_404(Comment, id=id)
    try:
        obj = Comment.objects.get(id=id)
    except:
        raise Http404

    if obj.user != request.user:
        # messages.success(request, "You have no Permission")
        response = HttpResponse("You don't have permission to do this")
        response.status_code = 403
        raise response

    if request.method == "POST":
        parent_obj_url = obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request, "Deleted")
        return HttpResponseRedirect(parent_obj_url)
    context = {
        "object": obj,
    }

    return render(request, "confirm_delete.html", context)