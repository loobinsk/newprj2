from preferences.registry import preferences, StringPreference
from django.utils.translation import ugettext_lazy as _


@preferences.register
class ImportFtpServer(StringPreference):
    name = _('FTP server')
    category = _('Import')


@preferences.register
class ImportFtpUser(StringPreference):
    name = _('FTP user')
    category = _('Import')


@preferences.register
class ImportFtpPassword(StringPreference):
    name = _('FTP password')
    category = _('Import')


@preferences.register
class ImportGoodsFile(StringPreference):
    name = _('FTP goods file')
    category = _('Import')


@preferences.register
class ImportPropertiesFile(StringPreference):
    name = _('FTP properties file')
    category = _('Import')


@preferences.register
class ImportImagesPath(StringPreference):
    name = _('FTP images path')
    category = _('Import')


@preferences.register
class ImportDescriptionsPath(StringPreference):
    name = _('FTP descriptions path')
    category = _('Import')


@preferences.register
class OrderEmail(StringPreference):
    name = _('Order e-mail')
    category = _('Mail settings')
