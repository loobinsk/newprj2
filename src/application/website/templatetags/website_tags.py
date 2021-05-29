from django import template

from ..models import BottomMenu, SocialIcon, StatisticCounter, BottomIcon, MainBlock, ShopAddresses

register = template.Library()


@register.inclusion_tag('tags/website.menu.bottom.html')
def website_menu_bottom():

    items = BottomMenu.cache.public()

    for i in items:
        i.has_child = False
        i.active = False

    for i in items:

        if i.parent_id:
            for p in items:
                if i.parent_id == p.id:
                    p.has_child = True

    return {'items': items}


@register.inclusion_tag('tags/website.menu.bottom.addresses.html')
def website_menu_bottom_addresses():

    items = ShopAddresses.objects.all()

    return {'items': items}


@register.inclusion_tag('tags/website.header.top.addresses.html')
def website_header_top_addresses():

    items = ShopAddresses.objects.all().first()

    return {'items': items}


@register.inclusion_tag('tags/website.social.icons.html')
def website_social_icons():

    items = SocialIcon.cache.public()

    return {'items': items}


@register.inclusion_tag('tags/website.statistics.counters.html')
def website_statistics_counters():

    items = StatisticCounter.cache.public()

    return {'items': items}


@register.inclusion_tag('tags/website.icons.bottom.html')
def website_icons_bottom():

    items = BottomIcon.cache.public()

    return {'items': items}


@register.inclusion_tag('tags/website.blocks.main.html')
def website_blocks_main():

    items = MainBlock.cache.public()

    return {'items': items}
