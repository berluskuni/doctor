# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-28 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinika', '0007_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='label',
            field=models.PositiveSmallIntegerField(blank=True, default=1),
        ),
    ]
