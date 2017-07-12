# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import PostForm
from comment.forms import CommentForm

from comment.models import Comment
from django.db.models import Q

# Create your views here.

def post_list(request):
    today = timezone.now()
    querysetlist = Post.objects.active().order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        querysetlist = Post.objects.all().order_by("-timestamp")
    query = request.GET.get("q")
    if query:
        querysetlist = querysetlist.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(category__icontains=query)
        ).distinct()
    paginator = Paginator(querysetlist,5)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)



    context = {
        "objects_list": queryset,
        "page_request_var": page_request_var,
        "title": "List",
        "today":today,


    }


    return render(request,"home.html", context)

def post_detail(request, slug=None):
    ins = get_object_or_404(Post,slug=slug)
    if ins.publish > timezone.now().date() or ins.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    initial_data = {
        "content_type": ins.get_content_type,
        "object_id": ins.id,
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


    comments = ins.comments

    context = {
        "instance": ins,
        "comments": comments,
        "comment_forms": comment_forms,

    }

    return render(request,"detail.html", context)

def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_authenticated:
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
    }
    return render(request,"post_form.html", context)

def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_authenticated:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)

def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_authenticated:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    return redirect("blog:home")

