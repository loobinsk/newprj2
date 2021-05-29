from django.db import models
from django.utils.translation import ugettext_lazy as _

from cache_model.models import CacheModel
from public_model.models import PublicModel
from sort_model.models import OrderModel


class StatisticCounter(CacheModel, OrderModel, PublicModel, models.Model):

    name = models.CharField(_('Name'), max_length=100)
    code = models.TextField(_('Html code'))

    object = models.Manager()

    class Meta:
        db_table = 'website_statistic_counters'
        ordering = ['order']
        verbose_name = _('Statistic counter')
        verbose_name_plural = _('Statistic counters')

    def __str__(self):
        return '%s' % self.name
