"""blogsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import post.views as post_views

urlpatterns = [

    url(r'^$',post_views.post_list, name="home"),
    url(r'^(?P<slug>[-\w]+)/$', post_views.post_detail, name="detail"),
    url(r'^create/',post_views.post_create, name="create" ),
    url(r'^(?P<slug>[-\w]+)/update/', post_views.post_update, name="update"),
    url(r'^(?P<slug>[-\w]+)/delete/', post_views.post_delete, name="delete"),
]
