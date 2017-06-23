# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import reverse
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

def upload_location(instance, filename):
    PostModel = instance.__class__
    new_id = PostModel.objects.order_by("id").last().id+1
    return "%s/%s" %(new_id, filename)

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True,null=True,blank=True)
    images = models.ImageField(upload_to=upload_location,
                               null=True,
                               blank=True,
                               width_field="width_field",
                               height_field="height_field"
                               )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    category = models.CharField(max_length=20)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail",kwargs={"slug":self.slug} )


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug=create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)


