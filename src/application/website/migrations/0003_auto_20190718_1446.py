# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-18 14:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_shopaddresses'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shopaddresses',
            options={'verbose_name': 'адрес', 'verbose_name_plural': 'Адреса в нижнем меню'},
        ),
        migrations.AlterField(
            model_name='bottommenu',
            name='level',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='bottommenu',
            name='lft',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='bottommenu',
            name='rght',
            field=models.PositiveIntegerField(editable=False),
        ),
    ]
