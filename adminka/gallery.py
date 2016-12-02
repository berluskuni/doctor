# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .decorators import *
from .forms import *
from django.core.files import uploadhandler, uploadedfile
from uuslug import slugify
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.cache import cache
from datetime import datetime, date, time, timedelta
from .apps import determine_role, get_paginator
from clinika.models import *
from .apps import *

# свой обработчик файлов
class MyUploadHandler(uploadhandler.FileUploadHandler):

    def __init__(self, *args, **kwargs):
        super(MyUploadHandler, self).__init__(*args, **kwargs)

    def new_file(self, *args, **kwargs):

        """
        Create the file object to append to as data is coming in.
        """
        super(MyUploadHandler, self).new_file(*args, **kwargs)

        translit = slugify(self.file_name)  # добавленная функцию транслитерации названия
        ind = translit.rfind('-')
        translit = translit[:ind] + '.' + translit[(ind + 1):]
        self.file_name = translit
        self.file = uploadedfile.TemporaryUploadedFile(self.file_name, self.content_type, 0, self.charset, self.content_type_extra)

    def receive_data_chunk(self, raw_data, start):
        self.file.write(raw_data)

    def file_complete(self, file_size):
        self.file.seek(0)
        self.file.size = file_size
        return self.file

@login_required
def media_all(request):
    user = request.user
    admin, staff = determine_role(user)
    images = Gallery.objects.all().order_by('-id')
    now = date.today()
    txt_date = "01.01." + str(2016)  # начало года
    date1 = datetime.strptime(txt_date, "%d.%m.%Y")

    images = get_paginator(request, images, 60)

    form_search = MediaForm(initial={'date1': date1, 'date2': now,})
    form_edit = MediaForm(initial={'extuser': user, })
    form = MediaForm(initial={'extuser': user, })

    return render(request, 'admin_media.html', {
        'form': form, 'form_search': form_search, 'form_edit': form_edit,
        'images': images, 'admin': admin, 'active': 'm1'
    })

# Редактирование медиа файла
@login_required
@edit_gallery_required
def image_edit(request, img_id):
    img = get_object_or_404(Gallery, pk=img_id)
    if request.method == 'POST':
        form = MediaEditForm(request.POST)
        if form.is_valid():
            form.full_clean()
            D = form.cleaned_data
            alt = D.get('seo_alt')
            file_preview_id = D.get('file_preview_id')
            if alt:
                img.seo_alt = alt
            if file_preview_id:
                try:
                    file_preview = get_object_or_404(Gallery, pk=int(file_preview_id))
                    img.file_preview = file_preview
                except:
                    a = 1
            img.save()
    return_path = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(return_path)

# Добавления медиа файла
# прогон через свой обработчик файлов на лету
@csrf_exempt
@login_required
@edit_gallery_required
def media_add(request):
    request.upload_handlers.insert(0, MyUploadHandler())
    path = '/adminka/media/'

    return _media_add(request, path)

# Добавление медиа файла
@csrf_protect
def _media_add(request, path=None):
    user = request.user
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            form.full_clean()
            D = form.cleaned_data
            file = D.get('file')
            mime_type, format_text = determine_atach_format(str(file))
            if mime_type != 'image':
                title = 'Неверный формат файла'
                message2 = """<p align="center"> <span class="error"> Должно быть изображение </span><br>
                Разрешенные форматы изображений: <strong> jpg, png, gif, bmp, psd, tiff, jpeg, raw, tga </strong></p>"""
                return render(request, 'access_denied.html', {
                    'title': title, 'message2': message2,
                })

            extuser = D.get('extuser')
            seo_alt = D.get('seo_alt')
            file_preview_id = D.get('file_preview_id')

            img = Gallery.objects.create(file=file)
            img.seo_alt = seo_alt
            if extuser:
                img.extuser = extuser
            else:
                img.extuser = user
            if file_preview_id:
                try:
                    file_previu = get_object_or_404(Gallery, pk=int(file_preview_id))
                    img.file_preview = file_previu
                except:
                    a = 1
            try:
                img.create_thumbnails()
            except:
                img.previu = 'uploads/none_previu.jpg'
                img.save()

    return HttpResponseRedirect(path)

# Поиск медиа файлов
@login_required
@admin_required
def media_search(request):
    current_user = request.user
    user_id = current_user.id
    images = Gallery.objects.all()
    if request.method == 'POST':
        form = MediaForm(request.POST)
        form.full_clean()
        D = form.cleaned_data
        extuser = D.get('extuser')

        if extuser:
            images = images.filter(extuser=extuser)
        date1 = D.get('date1')
        date2 = D.get('date2')
        days = timedelta(days=1)
        date_from = date1 - days
        date_to = date2 + days
        images = images.filter(created__gt=date_from).exclude(created__gt=date_to)

        data = {'D': D, 'images': images }

        key = 'media' + str(user_id)
        cache.set(key, data, 60 * 30)
        path = '/adminka/media/found/'

        return HttpResponseRedirect(path)

    else:
        path = '/adminka/media/'
        return _media_add(request, path)

@login_required
@admin_required
def media_found(request):
    user = request.user
    admin, staff = determine_role(user)
    key = 'media' + str(user.pk)
    data = cache.get(key)
    images = data.get('images')
    images = get_paginator(request, images, 60)
    D = data.get('D')

    form_search = MediaForm(initial=D)
    form_edit = MediaForm(initial={'extuser': user, })
    form = MediaForm(initial={'extuser': user, })

    return render(request, 'admin_media.html', {
        'form': form, 'form_search': form_search, 'form_edit': form_edit,
        'images': images, 'admin': admin, 'active': 'm1'
    })

# Удаление медиа файла
@login_required
@edit_gallery_required
def media_delete(request, img_id):
    path = '/adminka/media/'
    image_delete(img_id)

    return HttpResponseRedirect(path)

# ((((((((  Изображения временной страницы  ))))))))))))

@csrf_exempt
@login_required
@edit_temp_page_required
def image_edit_temp(request, img_id):
    request.upload_handlers.insert(0, MyUploadHandler())

    return _image_edit_temp(request, img_id)

# Добавление медиа файла
@csrf_protect
def _image_edit_temp(request, img_id):
    user = request.user
    img = get_object_or_404(Gallery, pk=img_id)
    return_path = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            form.full_clean()
            D = form.cleaned_data
            file = D.get('file')
            if file:
                mime_type, format_text = determine_atach_format(str(file))
                if mime_type != 'image':
                    title = 'Неверный формат файла'
                    message2 = """<p align="center"> <span class="error"> Должно быть изображение </span><br>
                    Разрешенные форматы изображений: <strong> jpg, png, gif, bmp, psd, tiff, jpeg, raw, tga </strong></p>"""
                    return render(request, 'access_denied.html', {
                        'title': title, 'message2': message2,
                    })
                if img.file:
                    file_del = img.file
                    default_storage.delete(file_del)
                img.file = file
                img.save()
            seo_alt = D.get('seo_alt')
            path = D.get('path')
            img.seo_alt = seo_alt
            img.extuser = user

            try:
                img.create_thumbnails()
            except:
                img.previu = 'uploads/none_previu.jpg'
                img.save()
            if path:
                return_path += path
    return HttpResponseRedirect(return_path)