# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-07 14:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20181207_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=75, null=True, unique=True, verbose_name='E-mail'),
        ),
    ]
