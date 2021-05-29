from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


from seo.admin import seo_model
from sort_model.admin import order_model
from public_model.admin import public_model
from mptt.admin import MPTTModelAdmin


from ..models import Category, Brand


@seo_model
@order_model
@public_model
@admin.register(Category)
class CategoryAdmin (MPTTModelAdmin, admin.ModelAdmin):

    list_display = ('name', 'title', 'slug', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': (('name', 'title'), 'slug', 'parent', 'image', 'content', 'content_bottom')
        }),
        (_('Display'), {
            'classes': ('collapse',),
            'fields': ('submenu_direction',)
        }),
    )
    search_fields = ['name', 'title', 'slug', 'content', 'content_bottom']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 1000


@seo_model
@public_model
@admin.register(Brand)
class BrandAdmin (admin.ModelAdmin):

    list_display = ('name', 'title', 'slug', 'is_popular', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': (('name', 'title'), 'slug', 'image', 'content', 'is_popular', )
        }),
    )
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'title', 'slug', 'content']
    list_filter = ('is_popular', )
