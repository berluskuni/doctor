from django.db import models
from sorl.thumbnail import get_thumbnail
from extuser.models import *


class Contact(models.Model):
    clinic_name = models.CharField(max_length=200, verbose_name='Название клиники', blank=True, null=True)
    clinic_service_one = models.CharField(max_length=200, verbose_name='Направление деятельности', blank=True, null=True)
    clinic_service_two = models.CharField(max_length=200, verbose_name='Направление деятельности', blank=True, null=True)
    phone_one = models.CharField(max_length=25, verbose_name='Телефон', blank=True, null=True)
    phone_two = models.CharField(max_length=25, verbose_name='Телефон', blank=True, null=True)
    time_work_one_hours_begin = models.CharField(max_length=25, verbose_name='Время начало работы часы пн-пт:', blank=True)
    time_work_one_minute_begin = models.CharField(max_length=25, verbose_name='Время начало работы минуты пн-пт:', blank=True)
    time_work_one_hours_end = models.CharField(max_length=25, verbose_name='Время конца работы часы пн-пт:', blank=True)
    time_work_one_minute_end = models.CharField(max_length=25, verbose_name='Время конца работы минуты пн-пт:', blank=True)
    time_work_two_hours_begin = models.CharField(max_length=25, verbose_name='Время начало работы часы сб:', blank=True)
    time_work_two_minute_begin = models.CharField(max_length=25, verbose_name='Время начало работы минуты сб:', blank=True)
    time_work_two_hours_end = models.CharField(max_length=25, verbose_name='Время конца работы часы сб:', blank=True)
    time_work_two_minute_end = models.CharField(max_length=25, verbose_name='Время конца работы минуты сб:', blank=True)
    time_work_three = models.CharField(max_length=25, verbose_name='Время работы вс:', blank=True)
    address_dig = models.CharField(max_length=512, verbose_name='Адрес клиники - район')
    address_street = models.CharField(max_length=512, verbose_name='Адрес клиники - улица')
    address_text = models.CharField(max_length=512, verbose_name='Адрес клиники - примечание')

    def __str__(self):
        return self.clinic_name


class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование услуги', blank=True, null=True)
    label = models.PositiveSmallIntegerField(blank=True)
    icon = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title


class Gallery(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d', blank=True, verbose_name=u'Изображение галереи',
                            max_length=300)
    file_preview = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    preview = models.FileField(max_length=300, blank=True)
    label = models.PositiveSmallIntegerField(blank=True, null=True)
    seo_alt = models.CharField(max_length=300, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    extuser = models.ForeignKey(ExtUser, on_delete=models.SET_NULL, null=True)

    def create_thumbnails(self):
        # if not self.preview:
        preview = get_thumbnail(self.file, '160x160', crop='center', quality=99)
        self.preview = preview.name
        self.save()


class News(models.Model):
    title_news = models.CharField(max_length=512, blank=True, verbose_name='Название новости')
    news_data_day = models.PositiveSmallIntegerField(verbose_name='День выхода новости')
    news_data_month = models.CharField(max_length=20, blank=True, verbose_name='Месяц выхода новости')
    description_news = models.TextField(max_length=512, blank=True, verbose_name='Описание новости')
    img_news = models.FileField(upload_to='uploads/%Y/%m/%d', blank=True, verbose_name=u'Изображение новости',
                                max_length=180)
    extuser = models.ForeignKey(ExtUser, on_delete=models.SET_NULL, null=True)
    label = models.PositiveSmallIntegerField(blank=True, default=1)

    def __str__(self):
        return self.title_news




