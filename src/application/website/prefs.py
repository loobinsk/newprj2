from preferences.registry import preferences, StringPreference
from django.utils.translation import ugettext_lazy as _


@preferences.register
class SiteName(StringPreference):
    name = _('Site name')
    category = _('Website settings')


@preferences.register
class SiteUrl(StringPreference):
    name = _('Site url')
    category = _('Website settings')


@preferences.register
class Slogan(StringPreference):
    name = _('Slogan')
    category = _('Website display')


@preferences.register
class Copyrights(StringPreference):
    name = _('Copyrights')
    category = _('Website display')


@preferences.register
class Phone(StringPreference):
    name = _('Phone')
    category = _('Website display')


@preferences.register
class SocialTitle(StringPreference):
    name = _('Social title')
    category = _('Website display')


@preferences.register
class BackgroundImageUrl(StringPreference):
    name = _('Background image url')
    category = _('Site display')
