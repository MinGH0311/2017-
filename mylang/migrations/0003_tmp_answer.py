# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-29 05:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mylang', '0002_history_recommand'),
    ]

    operations = [
        migrations.CreateModel(
            name='tmp_answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(default='')),
            ],
        ),
    ]
