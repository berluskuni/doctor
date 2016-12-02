# -*- coding: utf-8 -*-

from django import forms
from extuser.models import ExtUser
#from app_landing.models import *
from multiupload.fields import MultiFileField
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class MediaForm(forms.Form):

    file = forms.FileField(required=False)
    years = [2016, 2015]
    CHOOSE_YEARS = tuple(years)
    extuser = forms.ModelChoiceField(queryset=ExtUser.objects.all(), required=False,)
    date1 = forms.DateField(widget=forms.SelectDateWidget(years=CHOOSE_YEARS), required=False,)
    date2 = forms.DateField(widget=forms.SelectDateWidget(years=CHOOSE_YEARS), required=False,)
    title = forms.CharField(label='Заголовок', max_length=200, required=False)
    seo_description = forms.CharField(label='seo_description', max_length=200, required=False)
    seo_alt = forms.CharField(max_length=200, required=False)
    file_preview_id = forms.IntegerField(required=False)
    path = forms.CharField(label='Название', max_length=200, required=False)

class MediaEditForm(forms.Form):
    seo_alt = forms.CharField(max_length=200, required=False)
    author = forms.ModelChoiceField(queryset=ExtUser.objects.all(), required=False)
    file_preview_id = forms.IntegerField(required=False)



class TempEditForm(forms.Form):
    list = []
    for x in range(1, 9):
        L = (str(x), str(x))
        list.append(L)
    ICONS = tuple(list)

    icons = forms.ChoiceField(choices=ICONS, required=False)
    title = forms.CharField(label='Название', max_length=200, required=False)
    path = forms.CharField(label='Название', max_length=200, required=False)
    service_pk = forms.IntegerField(required=False)


class TempContactForm(forms.Form):
    contact_id = forms.IntegerField(required=False)
    clinic_name = forms.CharField(label='Название', max_length=200, required=False)
    time_11_hours = forms.IntegerField(required=False)
    time_11_minutes = forms.IntegerField(required=False)
    time_12_hours = forms.IntegerField(required=False)
    time_12_minutes = forms.IntegerField(required=False)
    time_21_hours = forms.IntegerField(required=False)
    time_21_minutes = forms.IntegerField(required=False)
    time_22_hours = forms.IntegerField(required=False)
    time_22_minutes = forms.IntegerField(required=False)

    phone_one = forms.CharField(label='Телефон', max_length=30, required=False)
    phone_two = forms.CharField(label='Телефон', max_length=30, required=False)

    clinic_service_one = forms.CharField(label='Телефон', max_length=200, required=False)
    clinic_service_two = forms.CharField(label='Телефон', max_length=200, required=False)

    address_dig = forms.CharField(label='Адрес- район', max_length=600, required=False)
    address_street = forms.CharField(label='Адрес- улица', max_length=600, required=False)
    address_text = forms.CharField(label='Адрес- примечание', max_length=600, required=False)

class TempNewsForm(forms.Form):
    extuser = forms.ModelChoiceField(queryset=ExtUser.objects.all(), required=False)
    news_data_day = forms.IntegerField(required=False)
    news_data_month = forms.CharField(max_length=30, required=False)
    description_news = forms.CharField(label='description_news', max_length=600, required=False)
    img_news = forms.FileField(required=False)
    title_news = forms.CharField(max_length=200, required=False)
    path = forms.CharField(label='Название', max_length=200, required=False)

class RegistrationForm(forms.Form):
    years = []
    x = 2011
    for y in range(90):
        x -= 1
        years.append(x)
    CHOOSE_YEARS = tuple(years)
    email = forms.EmailField(required=False)
    firstname = forms.CharField(label='Имя', max_length=40, required=False)
    lastname = forms.CharField(label='Фамилия', max_length=40, required=False)
    password0 = forms.CharField(label='Текущий пароль', required=False, widget=forms.PasswordInput)
    password1 = forms.CharField(label='Новый пароль', required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение', required=False, widget=forms.PasswordInput)
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=CHOOSE_YEARS), required=False)
    key = forms.CharField(max_length=200, required=False)

class UserPermissionsGroup(forms.Form):
    extuser = forms.ModelChoiceField(queryset=ExtUser.objects.all(), required=False)
    admin = forms.BooleanField(label='Администратор', required=False)
    edit_gallery = forms.BooleanField(label='Редактирование медиа библиотеки', required=False)
    edit_temp_page = forms.BooleanField(label='Редактирование временной страницы', required=False)

class ChangeProfileForm(forms.Form):
    years = []
    x = 2011
    for y in range(90):
        x -= 1
        years.append(x)
    CHOOSE_YEARS = tuple(years)

    firstname = forms.CharField(label='Имя', max_length=60, required=False)
    lastname = forms.CharField(label='Фамилия', max_length=60, required=False)
    middlename = forms.CharField(label='Отчество', max_length=60, required=False)
    user_pk = forms.IntegerField(required=False)
    phone = forms.CharField(label='Моб. телефон', max_length=24, required=False)
    email = forms.EmailField(required=False)
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=CHOOSE_YEARS), required=False)

    title = forms.CharField(max_length=200, required=False)
    value = forms.CharField(max_length=200, required=False)
    show_date_of_birth = forms.BooleanField(required=False)
    password0 = forms.CharField(label='Текущий пароль', required=False, widget=forms.PasswordInput)
    password1 = forms.CharField(label='Новый пароль', required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение', required=False, widget=forms.PasswordInput)