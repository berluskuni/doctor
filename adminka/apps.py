from django.apps import AppConfig
from django.shortcuts import render, get_object_or_404
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
from clinika.models import Gallery


class AdminkaConfig(AppConfig):
    name = 'adminka'


def image_delete(img_id):
    image = get_object_or_404(Gallery, pk=img_id)
    if image.file:
        default_storage.delete(image.file)
        if image.preview:
            default_storage.delete(image.preview)
    image.delete()

# Определение типа и формата файла
def determine_atach_format(name):
    image_formats = ['jpg', 'png', 'gif', 'bmp', 'psd', 'tiff', 'jpeg', 'raw', 'tga']
    doc_formats = ['txt', 'rtf', 'doc', 'pdf', 'psd', 'zip', 'rar', 'docx', 'dotx',
                   'pot', 'ppt', 'xls', 'xlsx', 'xlsm', 'xltx', 'xltm', 'ppsx', 'pptx',
                   ]
    ind = name.rfind('.')
    format_text = name[(ind + 1):]
    if format_text in image_formats:
        mime_type = 'image'
    elif format_text in doc_formats:
        mime_type = 'application'
    else:
        mime_type = 'none'

    return mime_type, format_text

# Пагинатор
def get_paginator(request, qw_models, num_forpage=30):
    # Создаем paginator
    paginator = Paginator(qw_models, num_forpage)
    page = request.GET.get('page')
    try:
        models = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        models = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        models = paginator.page(paginator.num_pages)
    return models

def random_passw(length=8):
    passw = ''
    for x in range(length):
        passw += random.choice('qwertyuiopasdfghjklzxcvbnm123456789-')
    return passw

# чистка номер пользовательсткого ввода номера телефона
def clean_phone_number(phone_number):
    if phone_number[0] == '+':
        phone_number = phone_number[1:]

    symbol_list = ['(', ')', '-', ' ']
    for x in symbol_list:
        if x in phone_number:
            phone_number = phone_number.replace(x, '')
    return phone_number

def determine_role(user):
    admin, staff = False, False
    if user.groups.filter(name='staff').exists():
        staff = True
    if user.groups.filter(name='admin').exists():
        admin = True
    return admin, staff

# очистка слова от символов (список символов в list)
def clean_word(word, list):
    for x in list:
        if x in word:
            word = word.replace(x, '')
    return word

def determine_age(user):
    date_of_birth = user.date_of_birth
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля',
              'августа', 'сентября', 'октября', 'ноября', 'декабря']
    age = (date_of_birth.today() - date_of_birth).days // 365
    date_of_birth = str(date_of_birth.day) + ' ' + months[date_of_birth.month - 1] + '  ' \
                + str(date_of_birth.year) + 'г.'
    return date_of_birth, age