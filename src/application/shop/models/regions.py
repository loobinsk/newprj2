from django.db import models
from django.utils.translation import ugettext_lazy as _
from public_model.models import PublicModel


class Region(PublicModel, models.Model):

    region_name = models.CharField(_('Region Name'), max_length=250, unique=True)
    default_region = models.BooleanField(default=False)

    class Meta:
        db_table = 'shop_regions_region'
        ordering = ['region_name']

    def save(self, *args, **kwargs):
        if self.default_region:
            qs = type(self).objects.filter(default_region=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            qs.update(default_region=False)

        super(Region, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % self.region_name


class Shop(PublicModel, models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    address = models.CharField(max_length=300)
    delivery = models.CharField(max_length=300, default="")
    goods_file = models.CharField(max_length=300)
    email = models.EmailField(default="")
    phone_number = models.CharField(max_length=25, default="")
    default_shop = models.BooleanField(default=False)

    class Meta:
        db_table = 'shop_regions_shop'

    def __str__(self):
        return '%s' % self.address

    def save(self, *args, **kwargs):
        if self.default_shop:
            qs = type(self).objects.filter(default_shop=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            qs.update(default_shop=False)

        super(Shop, self).save(*args, **kwargs)

    def is_default_shop(self):
        return self.default_shop


class PriceInShop(PublicModel, models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    good = models.ForeignKey('Good', on_delete=models.CASCADE)
    price = models.IntegerField(_('Price'), blank=True, default=0)
    price_card = models.IntegerField(_('Price card'), blank=True, default=0)
    count = models.IntegerField(_('Count'), default=0, blank=True)
    is_order = models.BooleanField(_('On order'), default=False, blank=True)
    is_sale = models.BooleanField(_('Is sale'), default=False, blank=True)
    is_new = models.BooleanField(_('Is new'), default=False, blank=True)
    is_hit = models.BooleanField(_('Is hit'), default=False, blank=True)

    class Meta:
        db_table = 'shop_regions_priceinshop'
        unique_together = ['shop', 'good']
