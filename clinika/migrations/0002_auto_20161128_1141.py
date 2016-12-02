# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-28 11:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinika', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='time_work_one_hours',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='time_work_one_minute',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='time_work_two_hours',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='time_work_two_minute',
        ),
        migrations.AddField(
            model_name='contact',
            name='time_work_one_hours_begin',
            field=models.CharField(blank=True, max_length=25, verbose_name='Время начало работы часы пн-пт:'),
        ),
        migrations.AddField(
            model_name='contact',
            name='time_work_one_hours_end',
            field=models.CharField(blank=True, max_length=25, verbose_name='Время конца работы часы пн-пт:'),
        ),
        migrations.AddField(
            model_name='contact',
            name='time_work_one_minute_begin',
            field=models.CharField(blank=True, max_length=25, verbose_name='Время начало работы минуты пн-пт:'),
        ),
        migrations.AddField(
            model_name='contact',
            name='time_work_one_minute_end',
            field=models.CharField(blank=True, max_length=25, verbose_name='Время конца работы минуты пн-пт:'),
        ),
        migrations.AddField(
            model_name='contact',
            name='time_work_two_hours_begin',
            field=models.CharField(blank=True, max_length=25, verbose_name='Время начало работы часы сб:'),
        ),
        migrations.AddField(
            model_name='contact',
            name='time_work_two_hours_end',
            field=models.CharField(blank=True, max_length=25, verbose_name='Время конца работы часы сб:'),
        ),
        migrations.AddField(
            model_name='contact',
            name='time_work_two_minute_begin',
            field=models.CharField(blank=True, max_length=25, verbose_name='Время начало работы минуты сб:'),
        ),
        migrations.AddField(
            model_name='contact',
            name='time_work_two_minute_end',
            field=models.CharField(blank=True, max_length=25, verbose_name='Время конца работы минуты сб:'),
        ),
    ]