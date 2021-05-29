from django.contrib import admin

from sort_model.admin import order_model
from public_model.admin import public_model

from ..models import Property


@order_model
@public_model
@admin.register(Property)
class PropertyAdmin (admin.ModelAdmin):

    list_display = ('name', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', )
        }),
    )
    search_fields = ['name']
