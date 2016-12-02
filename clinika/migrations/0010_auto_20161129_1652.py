# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 13:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinika', '0009_auto_20161129_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='gallery',
            name='seo_alt',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='file',
            field=models.FileField(blank=True, max_length=300, upload_to='uploads/%Y/%m/%d', verbose_name='Изображение галереи'),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='preview',
            field=models.FileField(blank=True, max_length=300, upload_to=''),
        ),
    ]