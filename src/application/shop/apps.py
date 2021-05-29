from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ShopConfig(AppConfig):
    name = 'application.shop'
    verbose_name = _('E-shop')
    label = 'shop'

    def ready(self):
        super(ShopConfig, self).ready()
        #from .models import Good
        #for i in Good.objects.all():
        #    i.save()
        #from .tasks import import_catalog_from_ftp
        #print(import_catalog_from_ftp())
