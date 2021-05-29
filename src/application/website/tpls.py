from pages.registry import templates, Template
from django.utils.translation import ugettext_lazy as _


@templates.register
class IndexPage(Template):
    name = _('Website page')
    file = 'page.html'


@templates.register
class MainPage(Template):
    name = _('Main page')
    file = 'main.html'
