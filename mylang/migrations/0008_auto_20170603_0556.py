# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-03 05:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mylang', '0007_auto_20170602_0504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='youtube',
            name='category',
        ),
        migrations.AddField(
            model_name='youtube',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
