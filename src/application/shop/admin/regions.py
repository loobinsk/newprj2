from django.contrib import admin

from ..models import Region, Shop


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    pass

