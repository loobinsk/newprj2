from django import template
from ..models import Region, Shop, Good, PriceInShop

register = template.Library()


@register.inclusion_tag('tags/shop.regions.html')
def shop_regions():
    items = Region.objects.all()
    return {'items': items}


@register.simple_tag
def show_region(region):
    region = Region.objects.get(id=region)
    return region


@register.inclusion_tag('tags/shop.all_shops_by_region.html')
def show_all_shops_by_region(region):
    shops = Shop.objects.filter(region=region)
    return {'shops': shops}


@register.inclusion_tag('tags/shop.checkout.shops_by_region.html')
def show_shops_by_region_for_checkout(region):
    shops = Shop.objects.filter(region=region)
    return {'shops': shops}

@register.inclusion_tag('tags/shop.shops_for_good_detail.html')
def show_shops_for_good_detail(region, good):
    shops = Shop.objects.filter(region=region)
    price_in_shops = PriceInShop.objects.filter(good=good, shop__in=shops)
    good.count_in_region = good.calc_count_in_region(region)

    if good.count_in_region > 0:
        shops = [item.shop for item in price_in_shops if item.count > 0]
    elif good.count_in_region <= 0 and good.calc_is_order_in_region(region):
        shops = [item.shop for item in price_in_shops if item.is_order]
    else:
        shops = []

    if len(shops) == 0:
        return {"shops": None}
    elif len(shops) == 1:
        return {"shop": shops[0]}
    else:
        return {"shops": shops}


@register.assignment_tag
def get_region(request, user):
    if user.is_anonymous:
        if request.session.get('region'):
            return request.session['region']
        else:
            return user.get_default_region()
    else:
        if user.region:
            return user.region
        else:
            return user.get_default_region()
