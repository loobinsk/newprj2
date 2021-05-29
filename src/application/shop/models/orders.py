from cache_model.models import CacheModel
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from public_model.models import PublicModel
from sorl.thumbnail import ImageField
from sort_model.models import OrderModel

from .users import User
from .goods import Good


class Payment(CacheModel, PublicModel, OrderModel, models.Model):

    name = models.CharField(_('Name'), max_length=100, unique=True)

    object = models.Manager()

    class Meta:
        db_table = 'shop_orders_payments'
        ordering = ['order']
        verbose_name = _('Payment method')
        verbose_name_plural = _('Payment methods')

    def __str__(self):
        return '%s' % self.name


class Delivery(CacheModel, PublicModel, OrderModel, models.Model):

    name = models.CharField(_('Name'), max_length=100, unique=True)
    show_address = models.BooleanField(_('Show address'), )

    object = models.Manager()

    class Meta:
        db_table = 'shop_orders_delivery'
        ordering = ['order']
        verbose_name = _('Delivery')
        verbose_name_plural = _('Delivery items')

    def __str__(self):
        return '%s' % self.name


class City(CacheModel, PublicModel, OrderModel, models.Model):

    name = models.CharField(_('Name'), max_length=100, unique=True)

    object = models.Manager()

    class Meta:
        db_table = 'shop_orders_cities'
        ordering = ['order']
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

    def __str__(self):
        return '%s' % self.name


class Order(models.Model):

    types = (
        (0, _('Purchase')),
        (1, _('Order')),
    )

    date_create = models.DateTimeField(_('Date order'), auto_now_add=True)
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.SET_NULL, blank=True, null=True)

    payment = models.CharField(_('Payment'), max_length=100)
    delivery = models.CharField(_('Delivery'), max_length=100)
    city = models.CharField(_('City'), max_length=100, blank=True, null=True)
    street = models.CharField(_('Street'), max_length=100, blank=True, null=True)
    house = models.CharField(_('House'), max_length=100, blank=True, null=True)
    apartment = models.CharField(_('Apartment'), max_length=100, blank=True, null=True)

    name = models.CharField(_('User name'), max_length=100)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_('Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.')
    )
    phone = models.CharField(_('Phone'), max_length=17, validators=[phone_regex])

    type = models.IntegerField(_('Type'), default=0, blank=True, choices=types)

    sum = models.FloatField(_('Sum'), blank=True, default=0)
    count = models.IntegerField(_('Count'), default=0, blank=True)

    class Meta:
        db_table = 'shop_orders'
        ordering = ['-date_create']
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    @property
    def order_type(self):
        return self.get_type_display()

    def __str__(self):
        return _('Order #%s') % self.id


class OrderGood(models.Model):

    order = models.ForeignKey(Order, verbose_name=_('Order'), on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=250)
    vendor_code = models.CharField(_('Vendor code'), max_length=100)
    url = models.CharField(max_length=400)
    image = ImageField(_('Image'), upload_to='shop/orders/', blank=True)
    price = models.IntegerField(_('Price'), blank=True, default=0)
    price_card = models.IntegerField(_('Price card'), blank=True, default=0)
    count = models.IntegerField(_('Count'), default=0, blank=True)
    good = models.ForeignKey(Good, verbose_name=_('Good'), on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'shop_orders_goods'
        ordering = ['-order__date_create', 'id']
        verbose_name = _('Order good')
        verbose_name_plural = _('Order goods')

    @property
    def total_cost(self):
        return self.count * self.price

    def __str__(self):
        return self.name
