from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from public_model.admin import public_model
from sort_model.admin import order_model

from ..models import Payment, Delivery, City, Order, OrderGood


@public_model
@order_model
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = ('name', )
    list_display_links = ('name',)

    fieldsets = (
        (None, {
            'fields': ('name', )
        }),
    )

    search_fields = ['name']


@public_model
@order_model
@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):

    list_display = ('name', 'show_address')
    list_display_links = ('name',)

    fieldsets = (
        (None, {
            'fields': ('name', 'show_address', )
        }),
    )

    search_fields = ['name']
    list_filter = ('show_address', )


@public_model
@order_model
@admin.register(City)
class CityAdmin(admin.ModelAdmin):

    list_display = ('name', )
    list_display_links = ('name',)

    fieldsets = (
        (None, {
            'fields': ('name', )
        }),
    )

    search_fields = ['name']


class OrderGoodInlineTabularAdmin (admin.StackedInline):

    model = OrderGood
    fields = ('name', 'vendor_code', 'url', 'image', 'price_card', 'count', 'good')
    extra = 0
    list_select_related = ('good', )
    raw_id_fields = ('good', )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_create', 'payment', 'delivery', 'city', 'name', 'phone', 'type', 'count', 'sum', )
    list_display_links = ('id', 'date_create', )

    fieldsets = (
        (None, {
            'fields': ('id', 'type', )
        }),
        (_('Sum'), {
            'fields': ('count', 'sum',)
        }),
        (_('Options'), {
            'fields': ('payment', 'delivery', )
        }),
        (_('User data'), {
            'fields': ('name', 'phone', 'user',)
        }),
        (_('Address'), {
            'fields': ('city', 'street', 'house', 'apartment',)
        }),
        (_('Dates'), {
            'fields': ('date_create',)
        }),
    )
    date_hierarchy = 'date_create'
    list_filter = ('type', 'payment', 'delivery', 'city',)
    readonly_fields = ['date_create', 'id']
    search_fields = ['name', 'city', 'payment', 'delivery', 'phone', 'user__phone', 'city', 'street', 'house',
                     'apartment', 'id']
    raw_id_fields = ['user']
    inlines = [OrderGoodInlineTabularAdmin, ]
