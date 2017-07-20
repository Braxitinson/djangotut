# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import (authenticate,
                                 login,
                                 logout,
                                 get_user_model)

from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm

# Create your views here.
def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    print (request.user.is_authenticated())
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        print (request.user.is_authenticated())

    return render(request, "login.html", {"form": form,"title": title})

def register_view(request):
    title = 'Register'
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect("/blog")


    return render(request, 'login.html', {"form":form,"title":title})

def logout_view(request):
    return render(request, 'login.html',{})