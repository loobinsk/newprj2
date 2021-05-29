import sys
import platform
import psutil

from copy import deepcopy
from datetime import date, datetime

import django
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from admin_tools.dashboard import modules, Dashboard
from application.shop.models import User

from server_resources.dashboard import ServerResourcesDashboardModule


today = date.today()


class StatOverviewDashboardModule(modules.DashboardModule):

    title = _('Overview')
    template = 'admin/dashboard/stat.overview.html'
    children = ['', ]

    def init_with_context(self, context):

        context['users_count'] = User.objects.count()
        context['users_count_day'] = User.objects.filter(date_joined__year=today.year, date_joined__month=today.month,
                                                         date_joined__day=today.day).count()
        context['users_count_month'] = User.objects.filter(date_joined__year=today.year,
                                                           date_joined__month=today.month).count()


class SoftwareInfoDashboardModule(modules.DashboardModule):

    title = _('Software Info')
    template = 'admin/dashboard/info.software.html'
    children = ['', ]

    def init_with_context(self, context):

        context['django_version'] = django.get_version()
        context['django_status'] = django.VERSION[3]
        context['python_version'] = sys.version
        context['os_version'] = ' '.join(platform.dist())

        m_list = []
        for app_name in settings.INSTALLED_APPS:
            if '.' not in app_name:
                try:
                    module_ = __import__('%s.__init__' % app_name)
                    version = ''
                    if hasattr(module_, '__version__'):
                        version = module_.__version__
                    if hasattr(module_, 'VERSION'):
                        version = module_.VERSION
                    m_list.append({'name': app_name, 'version': version})
                except ImportError:
                    pass

        context['modules'] = m_list


class InfoDashboardModule(modules.DashboardModule):

    title = _('System information')
    template = 'admin/dashboard/info.system.html'
    children = ['', ]

    def init_with_context(self, context):
        context['system_time'] = datetime.now()
        context['boot_time'] = datetime.fromtimestamp(psutil.boot_time())


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for website
    """

    def init_with_context(self, context):

        # Quick links
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            draggable=False,
            collapsible=False,
            deletable=False,
            children=deepcopy(settings.ADMIN_TOOLS_DASHBOARD_LINKS_MAIN_PAGE),
        ))

        # Applications
        for a in settings.ADMIN_TOOLS_APPLICATIONS:

            if a.get('external', False):
                for t in a['tabs']:
                    self.children.append(modules.ModelList(
                        title=t['title'],
                        models=t['models']
                    ))
            else:
                group = modules.Group(
                    title=a['title'],
                    display='tabs',
                    children=[]
                )
                self.children.append(group)
                for t in a['tabs']:
                    app_list = modules.ModelList(
                        title=t['title'],
                        models=t['models']
                    )
                    group.children.append(app_list)

        # Statistics
        self.children.append(modules.Group(
            title=_('Statistics'),
            display='tabs',
            children=[
                StatOverviewDashboardModule(),
                modules.ModelList(
                    title=_('Counters'),
                    models=settings.ADMIN_TOOLS_DASHBOARD_STATISTICS_MODELS
                ),
                modules.LinkList(
                    title=_('Other'),
                    children=deepcopy(settings.ADMIN_TOOLS_DASHBOARD_LINKS_STATISTICS),
                )
            ],
        ))

        # Technical information
        self.children.append(modules.Group(
            title=_('Technical information'),
            display='accordion',
            children=[
                ServerResourcesDashboardModule(),
                SoftwareInfoDashboardModule(),
                InfoDashboardModule(),
                modules.LinkList(
                    title=_('Support'),
                    children=deepcopy(settings.ADMIN_TOOLS_DASHBOARD_LINKS_SUPPORTS),
                )
            ]
        ))

        # Recent actions module
        self.children.append(modules.RecentActions(_('Recent Actions'), 5, enabled=False))
