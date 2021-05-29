from .statistics import *

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy

ADMIN_TOOLS_INDEX_DASHBOARD = 'application.dashboard.CustomIndexDashboard'
ADMIN_TOOLS_MENU = 'application.menu.CustomMenu'
ADMIN_TOOLS_THEMING_CSS = 'admin/css/theming.css'

ADMIN_TOOLS_DASHBOARD_LINKS_MAIN_PAGE = [
    {'title': _('Project start page'), 'url': '/', 'external': False},
    {'title': _('Clear cache'), 'url': reverse_lazy('clear_cache'), 'external': False},
    {'title': _('Change password'), 'url': reverse_lazy('admin:password_change'), 'external': False},
    {'title': _('Log out'), 'url': reverse_lazy('admin:logout'), 'external': False},
]

ADMIN_TOOLS_APPLICATIONS = (
    {
        'title': _('Web site'),
        'external': True,
        'tabs': (
            {
                'title': _('Text on site'),
                'models': ('pages.*', ),
            },
            {
                'title': _('Content'),
                'models': ('filebrowser.*', ),
            },
        )
    },
    {
        'title': _('E-Shop'),
        'tabs': (
            {
                'title': _('Orders'),
                'models': ('application.shop.models.orders.Order', ),
            },
            {
                'title': _('Data'),
                'models': ('application.shop.models.categories.*', 'application.shop.models.goods.Good',
                           'application.shop.models.properties.Property'),
            },
            {
                'title': _('Classifiers'),
                'models': ('application.shop.models.orders.Payment', 'application.shop.models.orders.City',
                           'application.shop.models.orders.Delivery', 'application.shop.models.regions.Region',
                           'application.shop.models.regions.Shop', ),
            },
        )
    },
    {
        'title': _('Administration'),
        'tabs': (
            {
                'title': _('Authentication'),
                'models': ('application.shop.models.users.*', 'django.contrib.auth.*'),
            },
            {
                'title': _('Site display'),
                'models': ('application.website.models.menu.*', 'application.website.models.socials.*',
                           'application.website.models.icons.*', 'application.website.models.blocks.*'),
            },
            {
                'title': _('Site management'),
                'models': ('preferences.models.*', 'cache_model.*'),
            },
        )
    },
)

# Site management support links
ADMIN_TOOLS_DASHBOARD_LINKS_SUPPORTS = [
    {'title': _('Developer e-mail'), 'url': 'mailto:mail@engine2.ru', 'external': True},
    {'title': _('Developer site'), 'url': 'http://engine2.ru/', 'external': True},
    {'title': _('Developer git repository'), 'url': 'https://bitbucket.org/rown/', 'external': True},
]

# Statistics links
ADMIN_TOOLS_DASHBOARD_STATISTICS_MODELS = ('application.website.models.statistics.*', )
ADMIN_TOOLS_DASHBOARD_LINKS_STATISTICS_EX = []
if YANDEX_METRIKA_URL:
    ADMIN_TOOLS_DASHBOARD_LINKS_STATISTICS_EX += [{'title': _('Yandex Metrika'), 'url': YANDEX_METRIKA_URL,
                                                   'external': True}, ]
if GOOGLE_ANALYTICS_URL:
    ADMIN_TOOLS_DASHBOARD_LINKS_STATISTICS_EX += [{'title': _('Google Analitics'), 'url': GOOGLE_ANALYTICS_URL,
                                                   'external': True}, ]
ADMIN_TOOLS_DASHBOARD_LINKS_STATISTICS = ADMIN_TOOLS_DASHBOARD_LINKS_STATISTICS_EX + [
    {'title': _('Server resources usage statistics'), 'url': reverse_lazy('server_resources_index'), 'external': False},
]

ADMIN_TOOLS_MENU_LINKS = (
    {
        'title': _('Links'),
        'links': ADMIN_TOOLS_DASHBOARD_LINKS_STATISTICS_EX + [
            {'title': _('Server resources'), 'url': reverse_lazy('server_resources_index'), 'external': False},
        ],
    },
)
