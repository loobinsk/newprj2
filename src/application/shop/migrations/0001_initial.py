# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-25 02:15
from __future__ import unicode_literals

import ckeditor.fields
import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('phone', models.CharField(max_length=17, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.', regex='^\\+?1?\\d{9,15}$')], verbose_name='Phone')),
                ('email', models.EmailField(blank=True, default='', max_length=75, verbose_name='E-mail')),
                ('name', models.CharField(blank=True, default='', max_length=100, verbose_name='User name')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Is staff')),
                ('date_joined', models.DateField(default=datetime.datetime.now, verbose_name='Date created')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'auth_user',
                'ordering': ['phone'],
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_title', models.CharField(blank=True, max_length=200, verbose_name='Meta Title')),
                ('meta_keywords', models.CharField(blank=True, max_length=200, verbose_name='Meta Keywords')),
                ('meta_description', models.CharField(blank=True, max_length=200, verbose_name='Meta Description')),
                ('meta_noindex', models.BooleanField(default=False, verbose_name='No index')),
                ('title', models.CharField(blank=True, max_length=150, verbose_name='Title')),
                ('content', ckeditor.fields.RichTextField(blank=True, verbose_name='Content')),
                ('last_modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Last modified')),
                ('is_public', models.BooleanField(default=True, verbose_name='Is public')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='System name')),
                ('image', sorl.thumbnail.fields.ImageField(blank=True, upload_to='shop/brands/', verbose_name='Image')),
                ('is_popular', models.BooleanField(default=False, verbose_name='Is popular')),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
                'db_table': 'shop_brand',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_title', models.CharField(blank=True, max_length=200, verbose_name='Meta Title')),
                ('meta_keywords', models.CharField(blank=True, max_length=200, verbose_name='Meta Keywords')),
                ('meta_description', models.CharField(blank=True, max_length=200, verbose_name='Meta Description')),
                ('meta_noindex', models.BooleanField(default=False, verbose_name='No index')),
                ('title', models.CharField(blank=True, max_length=150, verbose_name='Title')),
                ('content', ckeditor.fields.RichTextField(blank=True, verbose_name='Content')),
                ('last_modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Last modified')),
                ('is_public', models.BooleanField(default=True, verbose_name='Is public')),
                ('order', models.PositiveIntegerField(default=99999999, editable=False)),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('slug', models.SlugField(max_length=100, verbose_name='System name')),
                ('content_bottom', ckeditor.fields.RichTextField(blank=True, verbose_name='Content bottom')),
                ('submenu_direction', models.CharField(choices=[('left', 'Left'), ('right', 'Right')], default='left', max_length=5, verbose_name='Submenu direction')),
                ('image', sorl.thumbnail.fields.ImageField(blank=True, upload_to='shop/categories/', verbose_name='Image')),
                ('url', models.CharField(blank=True, editable=False, max_length=400)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Category', verbose_name='Parent')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'db_table': 'shop_category',
                'ordering': ['tree_id', 'lft'],
            },
        ),
        migrations.CreateModel(
            name='Good',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_title', models.CharField(blank=True, max_length=200, verbose_name='Meta Title')),
                ('meta_keywords', models.CharField(blank=True, max_length=200, verbose_name='Meta Keywords')),
                ('meta_description', models.CharField(blank=True, max_length=200, verbose_name='Meta Description')),
                ('meta_noindex', models.BooleanField(default=False, verbose_name='No index')),
                ('content', ckeditor.fields.RichTextField(blank=True, verbose_name='Content')),
                ('last_modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Last modified')),
                ('is_public', models.BooleanField(default=True, verbose_name='Is public')),
                ('name', models.CharField(max_length=250, verbose_name='Name')),
                ('title', models.CharField(blank=True, max_length=1000, verbose_name='Title')),
                ('vendor_code', models.CharField(max_length=100, unique=True, verbose_name='Vendor code')),
                ('slug', models.SlugField(max_length=300, unique=True, verbose_name='System name')),
                ('price', models.IntegerField(blank=True, default=0, verbose_name='Price')),
                ('price_card', models.IntegerField(blank=True, default=0, verbose_name='Price card')),
                ('count', models.IntegerField(blank=True, default=0, verbose_name='Count')),
                ('image', sorl.thumbnail.fields.ImageField(blank=True, upload_to='shop/goods/', verbose_name='Image')),
                ('is_sale', models.BooleanField(default=False, verbose_name='Is sale')),
                ('is_new', models.BooleanField(default=False, verbose_name='Is new')),
                ('is_hit', models.BooleanField(default=False, verbose_name='Is hit')),
                ('url', models.CharField(blank=True, editable=False, max_length=400)),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.Brand', verbose_name='Brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Good',
                'verbose_name_plural': 'Goods',
                'db_table': 'shop_goods',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='GoodImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_public', models.BooleanField(default=True, verbose_name='Is public')),
                ('order', models.PositiveIntegerField(default=99999999, editable=False)),
                ('name', models.CharField(max_length=250, verbose_name='Name')),
                ('image', sorl.thumbnail.fields.ImageField(upload_to='shop/goods/add/', verbose_name='Image')),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Good', verbose_name='Good')),
            ],
            options={
                'verbose_name': 'Good image',
                'verbose_name_plural': 'Goods images',
                'db_table': 'shop_goods_images',
                'ordering': ['good__id', 'order'],
            },
        ),
        migrations.CreateModel(
            name='GoodProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_public', models.BooleanField(default=True, verbose_name='Is public')),
                ('value', models.CharField(blank=True, db_index=True, max_length=250, verbose_name='Value')),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Good', verbose_name='Good')),
            ],
            options={
                'verbose_name': 'Good property',
                'verbose_name_plural': 'Good properties',
                'db_table': 'shop_good_properties',
                'ordering': ['property__order'],
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_public', models.BooleanField(default=True, verbose_name='Is public')),
                ('order', models.PositiveIntegerField(default=99999999, editable=False)),
                ('name', models.CharField(max_length=250, unique=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Property',
                'verbose_name_plural': 'Properties',
                'db_table': 'shop_properties',
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='goodproperty',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Property', verbose_name='Property'),
        ),
        migrations.AlterUniqueTogether(
            name='goodimage',
            unique_together=set([('name', 'good')]),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('parent', 'name'), ('parent', 'slug')]),
        ),
    ]
