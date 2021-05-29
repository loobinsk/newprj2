from django.contrib import admin

from sort_model.admin import order_model
from public_model.admin import public_model

from ..models import StatisticCounter


@order_model
@public_model
@admin.register(StatisticCounter)
class StatisticCounterAdmin (admin.ModelAdmin):

    list_display = ('name', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', 'code', )
        }),
    )
    search_fields = ('name', 'code', )
