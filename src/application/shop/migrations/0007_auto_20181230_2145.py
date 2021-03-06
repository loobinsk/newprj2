# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-30 21:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_city_delivery_order_ordergood_payment'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='city',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='delivery',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='payment',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='good',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.Good', verbose_name='Good'),
        ),
    ]
