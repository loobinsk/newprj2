from django.db import models
from django.utils.translation import ugettext_lazy as _

from public_model.models import PublicModel
from sort_model.models import OrderModel

from .goods import Good


class Property(PublicModel, OrderModel, models.Model):

    name = models.CharField(_('Name'), max_length=250, unique=True)

    class Meta:
        db_table = 'shop_properties'
        ordering = ['order']
        verbose_name = _('Property')
        verbose_name_plural = _('Properties')

    def __str__(self):
        return '%s' % self.name


class GoodProperty(PublicModel, models.Model):

    property = models.ForeignKey(Property, verbose_name=_('Property'), on_delete=models.CASCADE)
    good = models.ForeignKey(Good, verbose_name=_('Good'), on_delete=models.CASCADE)
    value = models.CharField(_('Value'), max_length=250, blank=True, db_index=True)

    class Meta:
        db_table = 'shop_good_properties'
        ordering = ['property__order']
        verbose_name = _('Good property')
        verbose_name_plural = _('Good properties')

    def __str__(self):
        return '%s' % self.property.name
