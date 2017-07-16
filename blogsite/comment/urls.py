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
import comment.views as comment_views

urlpatterns = [
    url(r'^(?P<id>\d+)/$', comment_views.comment_thread, name="comment_thread"),
    # url(r'^(?P<id>\d+)/update/', comment_views.comment_update, name="comment_update"),
    url(r'^(?P<id>\d+)/delete/', comment_views.comment_delete, name="comment_delete"),
]
