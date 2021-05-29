from django.db import models
from django.utils.translation import ugettext_lazy as _

from cache_model.models import CacheModel
from public_model.models import PublicModel
from sort_model.models import OrderModel


class SocialIcon(CacheModel, OrderModel, PublicModel, models.Model):

    name = models.CharField(_('Name'), max_length=100)
    url = models.CharField(_('Url'), max_length=250, default='/', blank=True)
    icon_name = models.CharField(_('Icon name'), max_length=2)

    object = models.Manager()

    class Meta:
        db_table = 'website_social_icons'
        ordering = ['order']
        verbose_name = _('Social icon')
        verbose_name_plural = _('Social icons')

    def __str__(self):
        return '%s' % self.name

    def get_absolute_url(self):
        return '%s' % self.url
