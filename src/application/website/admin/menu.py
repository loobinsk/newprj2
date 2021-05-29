from django.contrib import admin

from sort_model.admin import order_model
from public_model.admin import public_model
from mptt.admin import MPTTModelAdmin

from ..models import BottomMenu, ShopAddresses


@order_model
@public_model
@admin.register(BottomMenu)
class BottomMenuAdmin(MPTTModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'url',)
    list_display_links = ('name',)

    fieldsets = (
        (None, {
            'fields': ('name', 'parent', 'url',)
        }),
    )
    search_fields = ('name', 'url',)


@admin.register(ShopAddresses)
class ShopAddressesAdmin(admin.ModelAdmin):
    list_display = ('text',)
