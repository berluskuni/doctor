# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import MediaForm
from django.contrib.auth.models import Group, User
from extuser.models import *
from clinika.models import *


def do_1(request):
    return_path = request.META.get('HTTP_REFERER', '/')
    imgs = Gallery.objects.all()
    for img in imgs:
        img.create_thumbnails()
    return HttpResponseRedirect(return_path)

def do_2(request):
    return_path = request.META.get('HTTP_REFERER', '/')
    list_of_groups = [
        'admin',
        'staff',
    ]
    list_of_roles = [
        'Админ',
    ]
    for group in list_of_groups:
        if not Group.objects.filter(name=group).exists():
            Group.objects.create(name=group)
    admin_users = ExtUser.objects.filter(is_superuser=True)
    for user in admin_users:
        user.groups.add(Group.objects.get(name='admin'))

    for dolzh in list_of_roles:
        if not Role.objects.filter(title=dolzh).exists():
            Role.objects.create(title=dolzh)


    return HttpResponseRedirect(return_path)