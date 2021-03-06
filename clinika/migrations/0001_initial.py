# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-28 11:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clinic_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Название клиники')),
                ('clinic_service_one', models.CharField(blank=True, max_length=200, null=True, verbose_name='Направление деятельности')),
                ('clinic_service_two', models.CharField(blank=True, max_length=200, null=True, verbose_name='Направление деятельности')),
                ('phone_one', models.CharField(blank=True, max_length=25, null=True, verbose_name='Телефон')),
                ('phone_two', models.CharField(blank=True, max_length=25, null=True, verbose_name='Телефон')),
                ('time_work_one_hours', models.CharField(blank=True, max_length=25, verbose_name='Время работы часы пн-пт:')),
                ('time_work_one_minute', models.CharField(blank=True, max_length=25, verbose_name='Время работы минуты пн-пт:')),
                ('time_work_two_hours', models.CharField(blank=True, max_length=25, verbose_name='Время работы часы сб:')),
                ('time_work_two_minute', models.CharField(blank=True, max_length=25, verbose_name='Время работы минуты сб:')),
                ('time_work_three', models.CharField(blank=True, max_length=25, verbose_name='Время работы вс:')),
                ('address_dig', models.CharField(max_length=512, verbose_name='Адрес клиники - район')),
                ('address_street', models.CharField(max_length=512, verbose_name='Адрес клиники - улица')),
                ('address_text', models.CharField(max_length=512, verbose_name='Адрес клиники - примечание')),
            ],
        ),
    ]
