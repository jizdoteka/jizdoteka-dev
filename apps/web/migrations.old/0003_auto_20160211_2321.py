# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-11 23:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20160211_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journey',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date/time of start of journey'),
        ),
    ]
