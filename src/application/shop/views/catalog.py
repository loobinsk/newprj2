
from django.db.models import Prefetch, Subquery, OuterRef, Count, Q, Max, Min
from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.views.generic import DetailView, TemplateView, View

from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from pages.models import PageModule
from pages.views import ModuleViewMixin, PageViewMixin
from public_model.views import PublicMixin

from ..classes import GoodsRecently, Cart
from ..models import Category, Good, Brand, GoodProperty, Shop, PriceInShop
from ..utils import get_goods, get_goods_queryset, goods_context, get_properties, get_goods_prep, get_goods_prep_prop, \
    categories_sum, get_goods_price


class CategoryDetailView(PageViewMixin, PublicMixin, DetailView):

    model = Category
    template_name = 'shop/catalog.html'
    categories = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if 'goods' in context:
            if not context['goods'].object_list and not self.categories.count():
                return redirect(to='/bad-region/')
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):

        self.page = self.object

        context = super(CategoryDetailView, self).get_context_data(**kwargs)

        # Goods
        goods = get_goods(self.request, category=self.object)
        context['goods'] = goods

        context['shop_category'] = self.object.id

        cart = Cart(self.request)
        context['ids_in_cart'] = [int(g['id']) for g in cart.cart]

        # Categories
        context['categories'] = self.categories

        context = goods_context(self.request, context)

        return context

    def get_object(self, queryset=None):

        if queryset is None:
            queryset = self.get_queryset()
        self.history = []
        for slug_number in (1, 2, 3):
            slug_name = 'category_{}'.format(slug_number)
            slug = self.kwargs.get(slug_name)
            if slug:
                try:
                    if slug_number == 1:
                        target_category = queryset.get(slug=slug, parent__isnull=True)
                    else:
                        target_category = queryset.get(slug=slug, parent=target_category)
                    self.history.append(target_category)
                except queryset.model.DoesNotExist:
                    raise Http404()

        goods_for_categories = get_goods_queryset(self.request.user, self.request.session).filter(id__in=Subquery(
            Good.objects.filter(category_id=OuterRef('category_id')).values_list('id', flat=True)
        )).filter(Q(priceinshop__count__gte=1) | Q(is_order=True))
        region = self.request.user.region if self.request.user.is_authenticated else self.request.session.get('region')

        shops_in_region = Shop.objects.filter(region=region)
        categories_with_goods = Category.objects.filter(
            Q(good__is_public=True) &
            Q(good__priceinshop__shop__in=shops_in_region) &
            (Q(good__priceinshop__count__gte=1) | Q(good__is_order=True))).distinct()

        available_cats = {item.parent.id for item in categories_with_goods if item.parent }
        available_cats.update(categories_with_goods.values_list('id', flat=True))

        self.categories = Category.objects.filter(
            Q(is_public=True, parent=target_category, pk__in=available_cats),
            ).prefetch_related(
            Prefetch(
                'good_set',
                queryset=goods_for_categories,
                to_attr='goods'
            )
        )

        for cat in self.categories:
            for good in cat.goods:
                good.count_in_region = good.calc_count_in_region(region)
                good.price_card = good.get_price_card_for_region(region)
                good.is_order = good.calc_is_order_in_region(region)

        have_sub = False
        for i in self.categories:
            if i.get_children().count():
                have_sub = True
                break

        if have_sub:
            self.template_name = 'shop/categories.html'

        if self.categories and not have_sub:
            self.template_name = 'shop/categories_with_goods.html'

        return target_category


class BrandDetailView(PageViewMixin, PublicMixin, DetailView):

    model = Brand
    template_name = 'shop/brand.html'

    def get_context_data(self, **kwargs):

        self.page = self.object

        context = super(BrandDetailView, self).get_context_data(**kwargs)

        # Goods
        goods = get_goods(self.request, brand=self.object)
        context['goods'] = goods
        context['shop_brand'] = self.object.id

        cart = Cart(self.request)
        context['ids_in_cart'] = [int(g['id']) for g in cart.cart]

        context = goods_context(self.request, context, True)

        # Brands
        brands = Good.objects.filter(is_public=True, brand__is_public=True, brand__isnull=False).\
            order_by('brand__name').values_list('brand__name', 'brand__id', 'brand__slug').\
            annotate(bcount=Count('brand__id'))

        brands_d = []
        for i in brands:
            item = (i[0], i[1], i[3], self.object.id == i[1], i[2])
            brands_d.append(item)

        context['brands'] = brands_d

        return context


class GoodDetailView(PageViewMixin, PublicMixin, DetailView):

    model = Good

    def get_context_data(self, **kwargs):

        self.page = self.object

        context = super(GoodDetailView, self).get_context_data(**kwargs)

        history = [{'name': i.name, 'url': i.get_absolute_url()}
                   for i in self.object.category.get_ancestors(include_self=True)]
        context['history'] = history

        region = self.request.user.region if self.request.user.is_authenticated else self.request.session.get('region')
        shop_ids = context['good'].priceinshop_set.all().filter(shop__region=region).values('shop')
        shops = Shop.objects.filter(id__in=shop_ids)

        related_goods = Good.objects.filter(
            is_public=True, category=self.object.category
        ).filter(
            Q(priceinshop__shop__in=shops, priceinshop__count__gte=1) |
            Q(priceinshop__shop__in=shops, priceinshop__count__lt=1, priceinshop__is_order=True)
        ).distinct(
        ).exclude(
            id=self.object.id
        ).prefetch_related('category')[:10]
        for good in related_goods:
            good.price_card = good.get_price_card_for_region(region)
            good.count = good.calc_count_in_region(region)
            good.is_order = good.calc_is_order_in_region(region)

        context['related_goods'] = related_goods

        gr = GoodsRecently(self.request)
        gr.set(self.object.id)
        recent_goods = Good.objects.filter(
            is_public=True, id__in=gr.goods
        ).filter(
            Q(priceinshop__shop__in=shops, priceinshop__count__gte=1) |
            Q(priceinshop__shop__in=shops, priceinshop__count__lt=1, priceinshop__is_order=True)
        ).distinct(
        ).exclude(
            id=self.object.id
        ).prefetch_related('category')[:10]

        try:
            objects = dict([(obj.id, obj) for obj in recent_goods])
            ids = gr.goods.copy()
            ids.remove(self.object.id)
            sorted_objects = [objects[id] for id in ids]
            for good in recent_goods:
                good.price_card = good.get_price_card_for_region(region)
            context['recent_goods'] = sorted_objects
        except:
            context['recent_goods'] = []

        context['recent_goods_count'] = recent_goods.count()

        cart = Cart(self.request)
        context['ids_in_cart'] = [int(g['id']) for g in cart.cart]

        if len(shops) == 1:
            context['shop'] = shops[0]
            price_in_shop_obj = PriceInShop.objects.get(good=context['good'].id, shop=shops[0])
            context['good'].price_card = price_in_shop_obj.price_card
            context['good'].count_in_region = context['good'].calc_count_in_region(region)
            context['good'].is_order = context['good'].calc_is_order_in_region(region)
        elif len(shops) > 1:
            context['shops'] = shops
            price_in_shop_obj = PriceInShop.objects.get(good=context['good'].id, shop=shops[0])
            context['good'].price_card = price_in_shop_obj.price_card
            context['good'].count_in_region = context['good'].calc_count_in_region(region)
            context['good'].is_order = context['good'].calc_is_order_in_region(region)
        return context

    def get_queryset(self):
        qs = super(GoodDetailView, self).get_queryset().select_related('category', 'brand')
        if self.kwargs.get('category_3'):
            return qs.filter(
                category__slug=self.kwargs['category_3'], category__parent__slug=self.kwargs['category_2'],
                category__parent__parent__slug=self.kwargs['category_1']
            )
        if self.kwargs.get('category_2'):
            return qs.filter(
                category__slug=self.kwargs['category_2'], category__parent__slug=self.kwargs['category_1']
            )

        return qs.filter(category__slug=self.kwargs['category_1'])


class GoodAjaxView(DetailView):

    model = Good
    template_name = 'shop/ajax_good.html'

    def get_context_data(self, **kwargs):
        context = super(GoodAjaxView, self).get_context_data(**kwargs)
        region = self.request.user.region if self.request.user.is_authenticated else self.request.session.get('region')
        context['good'].price_card = context['good'].get_price_card_for_region(region)
        context['good'].count_in_region = context['good'].calc_count_in_region(region)
        cart = Cart(self.request)
        context['ids_in_cart'] = [int(g['id']) for g in cart.cart]

        return context


class SaleView(ModuleViewMixin, TemplateView):

    template_name = 'shop/catalog.html'
    module = 'shop_sale'

    def get_context_data(self, **kwargs):

        # History
        self.history = [PageModule.assign(self.module).history_item]

        context = super(SaleView, self).get_context_data(**kwargs)

        # Goods
        goods = get_goods(self.request, is_sale=True)
        context['goods'] = goods
        context['shop_is_sale'] = 'yes'
        context = goods_context(self.request, context, False)

        return context


class NewView(ModuleViewMixin, TemplateView):

    template_name = 'shop/catalog.html'
    module = 'shop_new'

    def get_context_data(self, **kwargs):

        # History
        self.history = [PageModule.assign(self.module).history_item]

        context = super(NewView, self).get_context_data(**kwargs)

        # Goods
        goods = get_goods(self.request, is_new=True)
        context['goods'] = goods
        context['shop_is_new'] = 'yes'
        context = goods_context(self.request, context, False)

        return context


class GoodsAjaxView(TemplateView):

    template_name = 'shop/ajax_catalog.html'
    goods = []

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(GoodsAjaxView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super(GoodsAjaxView, self).get_context_data(**kwargs)

        # Goods
        context['goods'] = self.goods

        return context

    def get(self, request, *args, **kwargs):

        category = self.request.GET.get('category')
        brand = self.request.GET.get('brand')
        is_sale = self.request.GET.get('is_sale') == 'yes'
        is_new = self.request.GET.get('is_new') == 'yes'
        search_q = self.request.GET.get('q')

        self.goods = get_goods(
            self.request, category=category, brand=brand, is_sale=is_sale, is_new=is_new, search_q=search_q
        )

        return super(GoodsAjaxView, self).get(request, *args, **kwargs)


class AjaxFiltersBrandsView(TemplateView):

    template_name = 'shop/ajax_filters_brands.html'
    brands = None

    def get_context_data(self, **kwargs):

        context = super(AjaxFiltersBrandsView, self).get_context_data(**kwargs)
        context['brands'] = self.brands

        return context

    def get(self, request, *args, **kwargs):

        category = self.request.GET.get('category')
        brand = self.request.GET.get('brand')
        is_sale = self.request.GET.get('is_sale') == 'yes'
        is_new = self.request.GET.get('is_new') == 'yes'

        goods = get_goods_prep_prop(request, category, brand, is_new, is_sale, is_brands=False)
        self.brands = list(goods.order_by('brand__name').values_list('brand__name', 'brand__id').annotate(
            bcount=Count('brand__id')).filter(brand__isnull=False))

        brands_c = request.GET.getlist('brands[]')
        brands_d = []
        for i in self.brands:
            i += (str(i[1]) in brands_c, )
            brands_d.append(i)
        self.brands = brands_d

        return super(AjaxFiltersBrandsView, self).get(request, *args, **kwargs)


class AjaxFiltersView(TemplateView):

    template_name = 'shop/ajax_filters.html'
    properties = None

    def get_context_data(self, **kwargs):

        context = super(AjaxFiltersView, self).get_context_data(**kwargs)
        context['properties'] = self.properties

        return context

    def get(self, request, *args, **kwargs):

        try:

            category = self.request.GET.get('category')
            brand = self.request.GET.get('brand')
            is_sale = self.request.GET.get('is_sale') == 'yes'
            is_new = self.request.GET.get('is_new') == 'yes'

            # Category
            goods = get_goods_prep(request, category, brand, is_new, is_sale)

            ids = goods.values_list('id', flat=True)
            gp = list(GoodProperty.objects.filter(good__in=ids).
                      filter(property__is_public=True, is_public=True).
                      values('value', 'property__name', 'property__id').
                      annotate(g_count=Count('good_id')))
            properties = get_properties(gp)

            p = request.GET.getlist('properties[]')

            if p:
                properties_ids = []

                for i in p:
                    p_id, p_value = i.split('|', maxsplit=1)
                    p_item = None
                    for s in properties_ids:
                        if s['id'] == p_id:
                            p_item = s
                    if not p_item:
                        properties_ids.append({'id': p_id, 'items': [p_value]})
                    else:
                        p_item['items'].append(p_value)

                g2a = []

                for i in properties_ids:

                    q_objects = Q()
                    for o in i['items']:
                        q_objects |= Q(value=o)
                    q_objects &= Q(property__id=i['id']) & q_objects
                    gp2 = GoodProperty.objects.filter(q_objects).extra(select={'id': 'good_id'}).values('id').distinct()
                    g2a.append(gp2)
                    gp = GoodProperty.objects.filter(good__in=ids).filter(property__is_public=True, is_public=True)
                    # gp = GoodProperty.objects.filter(good__category__id__in=categories, good__is_public=True).\
                    #     filter(property__is_public=True, good__count__gt=0, is_public=True)
                    for g2ai in g2a:
                        gp = gp.filter(good__id__in=g2ai)
                    gp = list(gp.values('value', 'property__name', 'property__id').annotate(g_count=Count('good_id')))
                    properties2 = get_properties(gp)

                    for pp in properties:
                        if str(pp['id']) == str(i['id']):
                            pp['lock'] = True

                    properties3 = []
                    for pp in properties:

                        if pp['lock']:
                            properties3.append(pp)
                        else:
                            for pp2 in properties2:
                                if str(pp['id']) == str(pp2['id']):
                                    properties3.append(pp2)
                    properties = properties3

                for i in p:
                    p_id, p_value = i.split('|', maxsplit=1)
                    for s in properties:
                        for s2 in s['items']:
                            if str(s2['value']) == str(p_value) and str(s['id']) == str(p_id):
                                s2['checked'] = True

            self.properties = properties

        except ValueError:
            return HttpResponseBadRequest(_('Bad request'))

        return super(AjaxFiltersView, self).get(request, *args, **kwargs)


class AjaxFiltersCategoriesView(TemplateView):

    template_name = 'shop/ajax_categories.html'
    categories = None
    categories_2 = None
    categories_3 = None

    def get_context_data(self, **kwargs):

        context = super(AjaxFiltersCategoriesView, self).get_context_data(**kwargs)
        context['categories_filter'] = self.categories
        context['categories_filter_2'] = self.categories_2
        context['categories_filter_3'] = self.categories_3

        return context

    def get(self, request, *args, **kwargs):

        brand = self.request.GET.get('brand')

        goods = get_goods_queryset(request.user, request.session)
        if brand:
            goods = goods.filter(brand=brand)

        c = goods.order_by('category__name').values_list(
            'category__name', 'category__id', 'category__order', 'category__parent__name', 'category__parent__id',
            'category__parent__order', 'category__parent__parent__name', 'category__parent__parent__id',
            'category__parent__parent__order'). \
            annotate(bcount=Count('category__id')).filter(category__isnull=False)

        get_cats = request.GET.getlist('categories[]')

        categories = []
        for i in c:
            c_name = None
            c_id = None
            c_order = None
            if i[7] is not None:
                c_id = i[7]
                c_name = i[6]
                c_order = i[8]
            if i[4] is not None and c_id is None:
                c_id = i[4]
                c_name = i[3]
                c_order = i[5]
            if i[1] is not None and c_id is None:
                c_id = i[1]
                c_name = i[0]
                c_order = i[2]
            categories.append({
                'name': c_name, 'id': c_id, 'count': i[9], 'order': c_order, 'checked': str(c_id) in get_cats
            })

        self.categories = categories_sum(categories)

        if len(get_cats) > 0:
            level1_cat = get_cats[0]
            c = goods.filter(Q(category__parent__id=level1_cat) | Q(category__parent__parent__id=level1_cat)).\
                order_by('category__name').values_list(
                'category__name', 'category__id', 'category__order', 'category__parent__name', 'category__parent__id',
                'category__parent__order', 'category__parent__parent__name'). \
                annotate(bcount=Count('category__id')).filter(category__isnull=False)
            categories = []
            for i in c:
                c_name = None
                c_id = None
                c_order = None
                if i[4] is not None and c_id is None and str(i[4]) != str(level1_cat):
                    c_id = i[4]
                    c_name = i[3]
                    c_order = i[5]
                if i[1] is not None and c_id is None:
                    c_id = i[1]
                    c_name = i[0]
                    c_order = i[2]
                categories.append({
                    'name': c_name, 'id': c_id, 'count': i[7], 'order': c_order, 'checked': str(c_id) in get_cats
                })
            self.categories_2 = categories_sum(categories)

        if len(get_cats) > 1:
            level2_cat = get_cats[1]
            c = goods.filter(Q(category__parent__id=level2_cat)).\
                order_by('category__name').values_list(
                'category__name', 'category__id', 'category__order'). \
                annotate(bcount=Count('category__id')).filter(category__isnull=False)
            categories = []
            for i in c:
                categories.append({
                    'name': i[0], 'id': i[1], 'count': i[3], 'order': i[2], 'checked': str(i[1]) in get_cats
                })
            self.categories_3 = categories_sum(categories)

        return super(AjaxFiltersCategoriesView, self).get(request, *args, **kwargs)


class AjaxFiltersPricesView(View):

    def get(self, request, *args, **kwargs):

        category = self.request.GET.get('category')
        brand = self.request.GET.get('brand')
        is_sale = self.request.GET.get('is_sale') == 'yes'
        is_new = self.request.GET.get('is_new') == 'yes'

        goods = get_goods_price(
            self.request, category=category, brand=brand, is_sale=is_sale, is_new=is_new
        )

        if goods.aggregate(Max('price_card'))['price_card__max']:
            price_max = goods.aggregate(Max('price_card'))['price_card__max']
        else:
            price_max = 10000
        if goods.aggregate(Min('price_card'))['price_card__min']:
            price_min = goods.aggregate(Min('price_card'))['price_card__min']
        else:
            price_min = 0
        if price_max == price_min:
            price_min = 0

        resp = {'price_min': price_min, 'price_max': price_max}

        return JsonResponse(resp)
