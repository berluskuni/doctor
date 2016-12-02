# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from clinika.models import *
from django.contrib.auth import authenticate, login, logout
from .decorators import *
from django.contrib.auth.decorators import login_required
from datetime import datetime, date, time, timedelta
from adminka.apps import image_delete, get_paginator, determine_atach_format, determine_role
from .forms import *
from django.core.files import uploadhandler, uploadedfile
from uuslug import slugify
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.cache import cache
from django.core.files.storage import default_storage
from .gallery import MyUploadHandler

@login_required
def page_temp_edit(request):
    user = request.user
    admin, staff = determine_role(user)
    images = []
    for x in range(1, 4):
        img = get_object_or_404(Gallery, label=x)
        images.append(img)
    context = {'service': Service.objects.all().order_by('label'),
               'news': News.objects.all().order_by('label'),
               'images': images,
               }

    contact = Contact.objects.get(pk=1)
    time_work = {
        'time_11_hours': contact.time_work_one_hours_begin,
        'time_11_minutes': contact.time_work_one_minute_begin,
        'time_12_hours': contact.time_work_one_hours_end,
        'time_12_minutes': contact.time_work_one_minute_end,
        'time_21_hours': contact.time_work_two_hours_begin,
        'time_21_minutes': contact.time_work_two_minute_begin,
        'time_22_hours': contact.time_work_two_hours_end,
        'time_22_minutes': contact.time_work_two_minute_end,
    }
    form = TempEditForm()
    form_contact = TempContactForm(initial={})
    icons_numbers = range(1, 9)
    return render(request, 'admin_pages_temp.html', {
        'context': context, 'contact': contact, 'active': 'pages', 'form': form, 'form_contact': form_contact,
        'page_title': 'Детский доктор', 'time_work': time_work, 'icons_numbers': icons_numbers, 'admin': admin
    })

@login_required
@edit_temp_page_required
def edit_temp_contacts(request):
    user = request.user
    return_path = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        form = TempContactForm(request.POST)
        if form.is_valid():
            form.full_clean()
            D = form.cleaned_data
            contact_id = D.get('contact_id')
            contact = get_object_or_404(Contact, pk=contact_id)
            clinic_name = D.get('clinic_name')
            time_11_hours = D.get('time_11_hours')
            time_11_minutes = D.get('time_11_minutes')
            time_12_hours = D.get('time_12_hours')
            time_12_minutes = D.get('time_12_minutes')
            time_21_hours = D.get('time_21_hours')
            time_21_minutes = D.get('time_21_minutes')
            time_22_hours = D.get('time_22_hours')
            time_22_minutes = D.get('time_22_minutes')

            phone_one = D.get('phone_one')
            phone_two = D.get('phone_two')

            clinic_service_one = D.get('clinic_service_one')
            clinic_service_two = D.get('clinic_service_two')

            address_dig = D.get('address_dig')
            address_street = D.get('address_street')
            address_text = D.get('address_text')
            if time_11_hours == 0:
                time_11_hours = '00'
            if time_12_hours == 0:
                time_12_hours = '00'
            if time_21_hours == 0:
                time_21_hours = '00'
            if time_22_hours == 0:
                time_22_hours = '00'
            if time_11_minutes == 0:
                time_11_minutes = '00'
            if time_12_minutes == 0:
                time_12_minutes = '00'
            if time_21_minutes == 0:
                time_21_minutes = '00'
            if time_22_minutes == 0:
                time_22_minutes = '00'
            contact.time_work_one_hours_begin = str(time_11_hours)
            contact.time_work_one_minute_begin = str(time_11_minutes)
            contact.time_work_one_hours_end = str(time_12_hours)
            contact.time_work_one_minute_end = str(time_12_minutes)
            contact.time_work_two_hours_begin = str(time_21_hours)
            contact.time_work_two_minute_begin = str(time_21_minutes)
            contact.time_work_two_hours_end = str(time_22_hours)
            contact.time_work_two_minute_end = str(time_22_minutes)
            if phone_one:
                contact.phone_one = phone_one
            else:
                contact.phone_one = ''
            if phone_two:
                contact.phone_two = phone_two
            else:
                contact.phone_two = ''

            if clinic_service_one:
                contact.clinic_service_one = clinic_service_one
            else:
                contact.clinic_service_one = ''
            if clinic_service_two:
                contact.clinic_service_two = clinic_service_two
            else:
                contact.clinic_service_two = ''
            contact.clinic_name = clinic_name

            if address_dig:
                contact.address_dig = address_dig
            else:
                contact.address_dig = ''
            if address_street:
                contact.address_street = address_street
            else:
                contact.address_street = ''
            if address_text:
                contact.address_text = address_text
            else:
                contact.address_text = ''
            contact.save()

            return HttpResponseRedirect(return_path)

# Редактировать Услугу
@login_required
@edit_temp_page_required
def page_temp_service_edit(request):
    user = request.user
    return_path = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        form = TempEditForm(request.POST)
        if form.is_valid():
            form.full_clean()
            D = form.cleaned_data
            service_pk = D.get('service_pk')
            path = D.get('path')
            service = get_object_or_404(Service, pk=service_pk)
            icons = D.get('icons')
            title = D.get('title')

            if icons:
                service.icon = icons
            if title:
                service.title = title
            if path:
                return_path += path
            service.save()

            return HttpResponseRedirect(return_path)
    return HttpResponseRedirect(return_path)

# Удалить Услугу
@login_required
@edit_temp_page_required
def page_temp_service_delete(request, service_id):
    return_path = request.META.get('HTTP_REFERER', '/')
    service = get_object_or_404(Service, pk=service_id)
    service.delete()
    return_path += '#services'
    return HttpResponseRedirect(return_path)

# Добавить Услугу
@login_required
@edit_temp_page_required
def page_temp_service_add(request):
    return_path = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        form = TempEditForm(request.POST)
        if form.is_valid():
            form.full_clean()
            D = form.cleaned_data
            title = D.get('title')
            path = D.get('path')
            if title:
                service = Service.objects.create(title=title, label=1)
                service.label = service.pk
                service.save()
            if path:
                return_path += path

    return HttpResponseRedirect(return_path)

# Редактирование новостей
@csrf_exempt
@login_required
@edit_temp_page_required
def edit_temp_news(request, news_id):
    request.upload_handlers.insert(0, MyUploadHandler())

    return _edit_temp_news(request, news_id)

# Редактирование новостей
@csrf_protect
def _edit_temp_news(request, news_id):
    user = request.user
    return_path = request.META.get('HTTP_REFERER', '/')
    news = get_object_or_404(News, pk=news_id)
    if request.method == 'POST':
        form = TempNewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.full_clean()
            D = form.cleaned_data
            title_news = D.get('title_news')
            path = D.get('path')
            news_data_day = D.get('news_data_day')
            news_data_month = D.get('news_data_month')
            description_news = D.get('description_news')
            img_news = D.get('img_news')
            news.title_news = title_news
            news.description_news = description_news
            news.news_data_day = news_data_day
            news.news_data_month = news_data_month
            news.extuser = user
            if img_news:
                mime_type, format_text = determine_atach_format(str(img_news))
                if mime_type != 'image':
                    title = 'Неверный формат файла'
                    message2 = """<p align="center"> <span class="error"> Должно быть изображение </span><br>
                                    Разрешенные форматы изображений: <strong> jpg, png, gif, bmp, psd, tiff, jpeg, raw, tga </strong></p>"""
                    return render(request, 'access_denied.html', {
                        'title': title, 'message2': message2,
                    })
                if news.img_news:
                    file_del = news.img_news
                    default_storage.delete(file_del)
                news.img_news = img_news
            news.save()
            if path:
                return_path += path
    return HttpResponseRedirect(return_path)