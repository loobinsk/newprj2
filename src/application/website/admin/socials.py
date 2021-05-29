from django.contrib import admin

from sort_model.admin import order_model
from public_model.admin import public_model

from ..models import SocialIcon


@order_model
@public_model
@admin.register(SocialIcon)
class SocialIconAdmin (admin.ModelAdmin):

    list_display = ('name', 'url', 'icon_name', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', 'url', 'icon_name', )
        }),
    )
    search_fields = ('name', 'url', 'icon_name', )
