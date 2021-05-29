from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from admin_tools.menu import items, Menu


class CustomMenu(Menu):
    """
    Custom menu for website
    """

    def init_with_context(self, context):

        # Index
        self.children.append(items.MenuItem(_('Dashboard'), reverse('admin:index')))
        self.children.append(items.Bookmarks())

        # Applications
        for a in settings.ADMIN_TOOLS_APPLICATIONS:
            item = items.MenuItem(a['title'], '')
            for t in a['tabs']:
                sub_item = items.ModelList(t['title'], models=t['models'])
                item.children.append(sub_item)
            self.children.append(item)

        # Links
        for l in settings.ADMIN_TOOLS_MENU_LINKS:
            item = items.MenuItem(l['title'], '')
            for ln in l['links']:
                link = items.MenuItem(ln['title'], ln['url'])
                item.children.append(link)
            self.children.append(item)

        return super(CustomMenu, self).init_with_context(context)
