from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class WebsiteConfig(AppConfig):
    name = 'application.website'
    verbose_name = _('Website content')
    label = 'website'

    def ready(self):
        super(WebsiteConfig, self).ready()

