from django.contrib import admin

from sort_model.admin import order_model
from public_model.admin import public_model

from ..models import MainBlock


@order_model
@public_model
@admin.register(MainBlock)
class MainBlockAdmin (admin.ModelAdmin):

    list_display = ('name', 'text', 'url', 'type', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', 'text', 'url', 'image', 'type', )
        }),
    )
    search_fields = ('name', 'text', 'url', )
    list_filter = ('type', )
