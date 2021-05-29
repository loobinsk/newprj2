from django import template
from django.db.models import Count
from django.db.models import Q
import collections

from ..classes import Cart
from ..forms import RegistrationForm, LoginForm, RestorePasswordForm, OrderForm
from ..models import Category, Brand, Good, Shop

register = template.Library()


@register.inclusion_tag('tags/shop.categories.html', takes_context=True)
def shop_categories(context, region):

    shops_in_region = Shop.objects.filter(region=region)
    items = Category.objects.filter(
        Q(is_public=True)&
        Q(good__is_public=True) &
        Q(good__priceinshop__shop__in=shops_in_region) &
        (Q(good__priceinshop__count__gte=1) | Q(good__is_order=True))).distinct()

    root_nodes = sorted(list({item.get_root() for item in items if item.is_public}), key=lambda x: x.order)

    parrent_nodes = {item.parent for item in items if item.is_public}
    categorie_tree = collections.OrderedDict()

    for category in root_nodes:
        categorie_tree[category] = {}
        categorie_tree[category]['children'] = collections.OrderedDict()

        for child in sorted(category.get_children(), key=lambda x: x.order):

            if child in items:
                categorie_tree[category]['children'][child] = {}
            if child in parrent_nodes:
                categorie_tree[category]['children'][child] = {}
                categorie_tree[category]['children'][child]['children'] = collections.OrderedDict()
                for sub_children in sorted(child.get_children(), key=lambda x: x.order):
                    if sub_children in items:
                        categorie_tree[category]['children'][child]['children'][sub_children] = {}

    return {'categories': categorie_tree, 'user': context['user'], 'request': context['request']}


@register.inclusion_tag('tags/shop.brands.popular.html')
def shop_brands_popular():

    items = Brand.cache.filter(is_popular=True)
    return {'items': items}


@register.inclusion_tag('tags/shop.goods.hit.html')
def shop_goods_hit(region):
    shops = Shop.objects.filter(region=region)
    items = Good.objects.filter(priceinshop__is_hit=True, priceinshop__shop__in=shops).distinct()[:10].prefetch_related('category')
    for item in items:
        item.price_card = item.get_price_card_for_region(region)
    return {'items': items}


@register.inclusion_tag('tags/shop.brands.html')
def shop_brands():
    items = Good.objects.filter(brand__isnull=False).values('brand__name', 'brand__slug').\
        annotate(total=Count('brand')).order_by('brand__name')
    return {'items': items}


@register.inclusion_tag('tags/shop.register.form.html')
def shop_register_form():
    return {'form': RegistrationForm()}


@register.inclusion_tag('tags/shop.login.form.html')
def shop_login_form():
    return {'form': LoginForm()}


@register.inclusion_tag('tags/shop.restore.password.form.html')
def shop_restore_password_form():
    return {'form': RestorePasswordForm()}


@register.inclusion_tag('tags/shop.order.form.html')
def shop_order_form():
    return {'form': OrderForm()}


@register.inclusion_tag('tags/shop.cart.html', takes_context=True)
def shop_cart(context):
    cart = Cart(context['request'])
    return {'cart': cart}


@register.filter
def running_total(goods_list):
    return sum(g.total_cost for g in goods_list)

