# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import PostForm
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
    context = {
        "instance": ins,

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

