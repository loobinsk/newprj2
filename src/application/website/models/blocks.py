from django.db import models
from django.utils.translation import ugettext_lazy as _

from cache_model.models import CacheModel
from public_model.models import PublicModel
from sorl.thumbnail import ImageField
from sort_model.models import OrderModel


class MainBlock(CacheModel, OrderModel, PublicModel, models.Model):

    TYPES = (
        ('', _('Category')),
        ('new', _('Is new')),
        ('sales', _('Is sale')),
    )

    name = models.CharField(_('Name'), max_length=100)
    text = models.TextField(_('Text'), blank=True)
    url = models.CharField(_('Url'), max_length=250, default='/', blank=True)
    image = ImageField(_('Image'), upload_to='website/blocks/', blank=True)
    type = models.CharField(_('Block type'), choices=TYPES, default='', max_length=5, blank=True)

    object = models.Manager()

    class Meta:
        db_table = 'website_blocks_main'
        ordering = ['order']
        verbose_name = _('Main page block')
        verbose_name_plural = _('Main page blocks')

    def __str__(self):
        return '%s' % self.name

    def get_absolute_url(self):
        return '%s' % self.url
