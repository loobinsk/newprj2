from django.contrib import admin

from sort_model.admin import order_model
from public_model.admin import public_model

from ..models import BottomIcon


@order_model
@public_model
@admin.register(BottomIcon)
class BottomIconAdmin (admin.ModelAdmin):

    list_display = ('name', 'url', 'icon_name', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', 'url', 'icon_name', )
        }),
    )
    search_fields = ('name', 'url', 'icon_name', )
