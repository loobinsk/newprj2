from django.db import models
from django.utils.translation import ugettext_lazy as _

from cache_model.models import CacheModel
from mptt.models import MPTTModel
from public_model.models import PublicModel
from sort_model.models import OrderModel


class BottomMenu(MPTTModel, CacheModel, OrderModel, PublicModel, models.Model):
    name = models.CharField(_('Name'), max_length=100)
    parent = models.ForeignKey('self', verbose_name=_('Parent'), null=True, blank=True)
    url = models.CharField(_('Url'), max_length=250, default='/', blank=True)

    object = models.Manager()

    class Meta:
        db_table = 'website_bottom_main'
        ordering = ['tree_id', 'lft']
        verbose_name = _('Bottom menu item')
        verbose_name_plural = _('Bottom menu')

    class MPTTMeta:
        order_insertion_by = ['order']

    def __str__(self):
        return '%s' % self.name

    def get_absolute_url(self):
        return '%s' % self.url

    class CacheMeta:
        cache_fields = [('parent_id', 'parent.id')]


class ShopAddresses(models.Model):
    text = models.TextField(_('Text'))

    class Meta:
        db_table = 'website_bottom_addresses'
        verbose_name = _('адрес')
        verbose_name_plural = _('Адреса в нижнем меню')

    def __str__(self):
        return self.text
