from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from django.core.urlresolvers import reverse

from public_model.models import PublicModel
from pages.models import CustomPage
from sorl.thumbnail import ImageField
from sort_model.models import OrderModel
from cache_model.models import CacheModel

from .categories import Category, Brand
from .regions import Region, Shop, PriceInShop


class Good(CacheModel, PublicModel, CustomPage):

    name = models.CharField(_('Name'), max_length=250)
    title = models.CharField(_('Title'), max_length=1000, blank=True)
    vendor_code = models.CharField(_('Vendor code'), max_length=100, unique=True)
    slug = models.SlugField(_('System name'), max_length=300, unique=True)

    category = models.ForeignKey(Category, verbose_name=_('Category'), on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, verbose_name=_('Brand'), on_delete=models.SET_NULL, blank=True, null=True)

    price = models.IntegerField(_('Price'), blank=True, default=0)
    price_card = models.IntegerField(_('Price card'), blank=True, default=0)
    count = models.IntegerField(_('Count'), default=0, blank=True)

    image = ImageField(_('Image'), upload_to='shop/goods/', blank=True)

    is_sale = models.BooleanField(_('Is sale'), default=False, blank=True)
    is_new = models.BooleanField(_('Is new'), default=False, blank=True)
    is_hit = models.BooleanField(_('Is hit'), default=False, blank=True)
    is_order = models.BooleanField(_('On order'), default=False, blank=True)

    url = models.CharField(max_length=400, blank=True, editable=False)

    objects = models.Manager()

    class Meta:
        db_table = 'shop_goods'
        ordering = ['id']
        verbose_name = _('Good')
        verbose_name_plural = _('Goods')

    def get_absolute_url(self):

        if self.category.parent is None:
            return reverse('shop:good', kwargs={'category_1': self.category.slug, 'slug': self.slug})
        if self.category.parent is not None and self.category.parent.parent is None:
            return reverse('shop:good', kwargs={'category_1': self.category.parent.slug,
                                                'category_2': self.category.slug, 'slug': self.slug})
        else:
            return reverse('shop:good', kwargs={'category_1': self.category.parent.parent.slug,
                                                'category_2': self.category.parent.slug,
                                                'category_3': self.category.slug, 'slug': self.slug})

    @cached_property
    def properties(self):
        return self.goodproperty_set.prefetch_related('property').filter(is_public=True)

    @cached_property
    def images_list(self):
        return self.goodimage_set.filter(is_public=True)

    def save(self, *args, **kwargs):
        self.url = self.get_absolute_url()
        super(Good, self).save(*args, **kwargs)

    def update_count(self):
        count = 0

        for price_in_shop_obj in self.priceinshop_set.all():
            count += price_in_shop_obj.count
            self.count = count
            self.save()

    def get_price_card_for_region(self, user_region):
        try:
            price_in_shop = self.priceinshop_set.filter(shop__region=user_region)[0]
            price_card = price_in_shop.price_card
        except:
            price_card = self.price_card
        return price_card

    def calc_count_in_region(self, region):
        prices_in_shops = self.priceinshop_set.filter(shop__region=region)
        count_in_shops = 0
        for item in prices_in_shops:
            count_in_shops += item.count
        return count_in_shops

    def calc_is_order_in_region(self, region):
        prices_in_shops = self.priceinshop_set.filter(shop__region=region)
        return any([item.is_order for item in prices_in_shops])


class GoodImage(PublicModel, OrderModel, models.Model):

    name = models.CharField(_('Name'), max_length=250)
    good = models.ForeignKey(Good, verbose_name=_('Good'), on_delete=models.CASCADE)
    image = ImageField(_('Image'), upload_to='shop/goods/add/')

    class Meta:
        db_table = 'shop_goods_images'
        ordering = ['good__id', 'order']
        verbose_name = _('Good image')
        verbose_name_plural = _('Goods images')
        unique_together = (('name', 'good'), )

    def __str__(self):
        return '%s' % self.image
