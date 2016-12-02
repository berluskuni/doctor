# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse

def super_user_required(function):
    def check(request, **kwargs):
        user = request.user
        if user.is_superuser:
            return function(request, **kwargs)
        else:
            message1 = 'Доступ закрыт'
            message2 = "Недостаточно прав"
            title = 'Доступ закрыт'
            return render(request,'access_denied.html', {
                'message1': message1, 'message2': message2, 'title': title,})
    return check

# Редактирование проекта
def admin_required(function):
    def check(request, **kwargs):
        user = request.user
        if user.groups.filter(name='admin'):
            return function(request, **kwargs)
        else:
            message1 = 'Доступ закрыт'
            message2 = "Недостаточно прав"
            title = 'Доступ закрыт'

            return render(request, 'access_denied.html', {
                'message1': message1, 'message2': message2, 'title': title,})
    return check



# Редактирование медиа библиотеки
def edit_gallery_required(function):
    def check(request, **kwargs):
        user = request.user
        if user.groups.filter(name='edit_gallery'):
            return function(request, **kwargs)
        else:
            message1 = 'Доступ закрыт'
            message2 = "Недостаточно прав"
            title = 'Доступ закрыт'

            return render(request, 'access_denied.html', {
                'message1': message1, 'message2': message2, 'title': title,})
    return check

# Редактирование временной страницы
def edit_temp_page_required(function):
    def check(request, **kwargs):
        user = request.user
        if user.groups.filter(name='edit_temp_page'):
            return function(request, **kwargs)
        else:
            message1 = 'Доступ закрыт'
            message2 = "Недостаточно прав"
            title = 'Доступ закрыт'

            return render(request, 'access_denied.html', {
                'message1': message1, 'message2': message2, 'title': title,})
    return check