from django.db.models import Prefetch, Q, Max, Min, Count
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.safestring import mark_safe

from ..models import Good, GoodImage, GoodProperty, Region, Shop


def get_goods_queryset(user=None, session=None):
    region = user.region if user.is_authenticated else session.get('region')
    shops_in_region = Shop.objects.filter(region=region)
    goods_filter = Good.objects.filter(is_public=True, priceinshop__shop__in=shops_in_region).distinct()

    goods = goods_filter.prefetch_related('brand').prefetch_related(
            Prefetch(
                'goodimage_set',
                queryset=GoodImage.objects.filter(is_public=True),
                to_attr='images'
            )
        )

    return goods


def get_goods_price(request, category=None, brand=None, is_new=None, is_sale=None):

    goods = get_goods_queryset(request.user, request.session)

    # Categories
    get_cats = request.GET.getlist('categories[]')
    if get_cats:
        if len(get_cats) > 2:
            goods = goods.filter(category=get_cats[2])
        elif len(get_cats) > 1:
            goods = goods.filter(Q(category=get_cats[1]) | Q(category__parent=get_cats[1]))
        else:
            goods = goods.filter(Q(category=get_cats[0]) | Q(category__parent=get_cats[0]) |
                                 Q(category__parent__parent=get_cats[0]))

    # Category
    if category is not None and category != '':
        goods = goods.filter(category=category)


    # Brand
    if brand is not None and brand != '':
        goods = goods.filter(brand=brand)

    region = request.user.region if request.user.is_authenticated else request.session.get('region')
    shops = Shop.objects.filter(region=region)

    # New and sale
    if is_new is not None and is_new:
        goods = goods.filter(priceinshop__is_new=is_new, priceinshop__shop__in=shops)
    if is_sale is not None and is_sale:
        goods = goods.filter(priceinshop__is_sale=is_sale, priceinshop__shop__in=shops)

    # Constant filters
    # First place
    if 'avail[]' in request.GET:
        q_objects = Q()
        for i in request.GET.getlist('avail[]'):
            if i == 'avail':
                # q_objects.add(Q(count__gte=1, is_order=False), Q.OR)
                q_objects.add(
                    Q(priceinshop__count__gte=1, priceinshop__shop__in=shops),
                    Q.OR
                )
            if i == 'order':
                # q_objects.add(Q(is_order=True), Q.OR)
                q_objects.add(
                    Q(priceinshop__is_order=True, priceinshop__count__lte=0, priceinshop__shop__in=shops),
                    Q.OR
                )
        goods = goods.filter(q_objects)
    else:
        goods = goods.filter(
            Q(priceinshop__is_order=True, priceinshop__count__lte=0, priceinshop__shop__in=shops) |
            Q(priceinshop__count__gte=1, priceinshop__shop__in=shops) |
            Q()
        )

    if 'actual[]' in request.GET:
        q_objects = Q()
        for i in request.GET.getlist('actual[]'):
            if i == 'new':
                q_objects.add(
                    Q(priceinshop__is_new=True, priceinshop__shop__in=shops),
                    Q.OR
                )
            if i == 'sale':
                q_objects.add(
                    Q(priceinshop__is_sale=True, priceinshop__shop__in=shops),
                    Q.OR
                )
        goods = goods.filter(q_objects)

    # Brands
    brands = request.GET.getlist('brands[]')
    q_objects = Q()
    for i in brands:
        q_objects |= Q(brand__id=i)
    goods = goods.filter(q_objects)

    return goods


def get_goods_prep(request, category=None, brand=None, is_new=None, is_sale=None, search_q=None, is_brands=True,
                   is_categories=True):

    goods = get_goods_queryset(request.user, request.session)

    # Categories
    if is_categories:
        get_cats = request.GET.getlist('categories[]')
        if get_cats:
            if len(get_cats) > 2:
                goods = goods.filter(category=get_cats[2])
            elif len(get_cats) > 1:
                goods = goods.filter(Q(category=get_cats[1]) | Q(category__parent=get_cats[1]))
            else:
                goods = goods.filter(Q(category=get_cats[0]) | Q(category__parent=get_cats[0]) |
                                     Q(category__parent__parent=get_cats[0]))

    # Category
    if category is not None and category != '':
        goods = goods.filter(category=category)

    # Brand
    if brand is not None and brand != '':
        goods = goods.filter(brand=brand)

    region = request.user.region if request.user.is_authenticated else request.session.get('region')
    shops = Shop.objects.filter(region=region)

    # New and sale
    if is_new is not None and is_new:
        # It works only for page "New" but not in case when user set filter "New"
        goods = goods.filter(priceinshop__is_new=is_new, priceinshop__shop__in=shops)
    if is_sale is not None and is_sale:
        # It works only for page "Sale" but not in case when user set filter "Sale"
        goods = goods.filter(priceinshop__is_sale=is_sale, priceinshop__shop__in=shops)
        # goods = goods.filter(is_sale=is_sale)

    # Search
    if 'q' in request.GET and request.GET['q']:
        search_q = request.GET['q']
        goods = goods.filter(Q(title__search=search_q) | Q(name__search=search_q) | Q(vendor_code=search_q) |
                             Q(title__icontains=search_q) | Q(name__icontains=search_q) | Q(vendor_code__icontains=search_q))

    # Constant filters
    # Second place
    if 'avail[]' in request.GET:
        q_objects = Q()
        for i in request.GET.getlist('avail[]'):
            if i == 'avail':
                # q_objects.add(Q(count__gte=1, is_order=False), Q.OR)
                q_objects.add(
                    Q(priceinshop__count__gte=1, priceinshop__shop__in=shops),
                    Q.OR
                )
            if i == 'order':
                # q_objects.add(Q(is_order=True), Q.OR)
                q_objects.add(
                    Q(priceinshop__is_order=True, priceinshop__count__lte=0, priceinshop__shop__in=shops),
                    Q.OR
                )
        goods = goods.filter(q_objects)
    else:
        # goods = goods.filter(Q(is_order=True) | Q(count__gte=1) | Q())
        goods = goods.filter(
            Q(priceinshop__is_order=True, priceinshop__count__lte=0, priceinshop__shop__in=shops) |
            Q(priceinshop__count__gte=1, priceinshop__shop__in=shops) |
            Q()
        )

    if 'actual[]' in request.GET:
        q_objects = Q()
        for i in request.GET.getlist('actual[]'):
            if i == 'new':
                q_objects.add(
                    Q(priceinshop__is_new=True, priceinshop__shop__in=shops),
                    Q.OR
                )
            if i == 'sale':
                q_objects.add(
                    Q(priceinshop__is_sale=True, priceinshop__shop__in=shops),
                    Q.OR
                )
        goods = goods.filter(q_objects)

    # Price
    if 'price[]' in request.GET:
        prices = request.GET.getlist('price[]')
        try:
            min_price = int(prices[0])
            max_price = int(prices[1])
            goods = goods.filter(
                priceinshop__price_card__gte=min_price,
                priceinshop__price_card__lte=max_price,
                priceinshop__shop__in=shops,
            )
        except:
            pass

    # Brands
    if is_brands:
        brands = request.GET.getlist('brands[]')
        q_objects = Q()
        for i in brands:
            q_objects |= Q(brand__id=i)
        goods = goods.filter(q_objects)

    return goods


def get_goods_prep_prop(request, category=None, brand=None, is_new=None, is_sale=None, search_q=None, is_brands=True,
                        is_categories=True):

    goods = get_goods_prep(request, category, brand, is_new, is_sale, search_q, is_brands, is_categories)

    properties = request.GET.getlist('properties[]')

    if properties:
        properties_ids = {}

        for i in properties:
            p_id, p_value = i.split('|', maxsplit=1)
            items = properties_ids.get(p_id, [])
            items.append(p_value)
            properties_ids[p_id] = items

        for i, v in properties_ids.items():
            q_objects = Q()
            for o in v:
                q_objects |= Q(value=o)
            q_objects &= Q(property__id=i) & q_objects
            gp = GoodProperty.objects.filter(q_objects).extra(select={'id': 'good_id'}).values('id').distinct()
            c = goods.filter(id__in=gp).count()
            if c > 0:
                goods = goods.filter(id__in=gp)

    return goods


def get_goods(request, category=None, brand=None, is_new=None, is_sale=None, search_q=None, page_count=None,
              is_brands=True):

    show_count = page_count
    goods = get_goods_prep_prop(request, category, brand, is_new, is_sale, search_q, is_brands)

    # Sort
    if 'sort_direction' in request.GET and request.GET['sort_direction'] in ['asc', 'desc']:
        request.session['shop_sort_direction'] = request.GET['sort_direction']
        sort_direction = request.GET['sort_direction']
    elif 'shop_sort_direction' in request.session:
        sort_direction = request.session['shop_sort_direction']
    else:
        sort_direction = settings.SHOP_SORT_DEFAULT_DIRECTION

    if 'sort_field' in request.GET and request.GET['sort_field'] in ['name', 'price']:
        request.session['shop_sort_field'] = request.GET['sort_field']
        sort_field = request.GET['sort_field']
    elif 'shop_sort_field' in request.session:
        sort_field = request.session['shop_sort_field']
    else:
        sort_field = settings.SHOP_SORT_DEFAULT_FIELD

    if sort_field == 'price':
        sort_field = 'priceinshop__price_card'

    if sort_direction == 'desc':
        sort_field = '-%s' % sort_field

    goods = goods.order_by(sort_field, 'id')

    # On page
    if not show_count:
        if 'show_count' in request.GET and request.GET['show_count'] in settings.SHOP_SHOW_COUNT:
            show_count = request.GET['show_count']
            request.session['shop_show_count'] = request.GET['show_count']
        elif 'shop_show_count' in request.session:
            show_count = request.session['shop_show_count']
        else:
            show_count = settings.SHOP_SHOW_COUNT_DEFAULT

        try:
            show_count = int(show_count)
        except ValueError:
            show_count = settings.SHOP_SHOW_COUNT_DEFAULT

    # Paginator
    paginator = Paginator(goods, show_count)
    page = request.GET.get('page', 1)
    try:
        items = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        items = paginator.page(1)

    region = request.user.region if request.user.is_authenticated else request.session.get('region')
    for good in items.object_list:
        good.price_card = good.get_price_card_for_region(region)
        good.count_in_region = good.calc_count_in_region(region)
        good.is_order = good.calc_is_order_in_region(region)

    items.object_list = [
        good for good in items.object_list
        if good.count_in_region > 0 or (good.count_in_region <= 0 and good.is_order)
    ]

    return items


def goods_context(request, context, properties=True):

    if 'shop_sort_field' in request.session:
        shop_sort_field = request.session['shop_sort_field']
    else:
        shop_sort_field = settings.SHOP_SORT_DEFAULT_FIELD
    context['shop_sort_field'] = shop_sort_field

    if 'shop_sort_direction' in request.session:
        shop_sort_direction = request.session['shop_sort_direction']
    else:
        shop_sort_direction = settings.SHOP_SORT_DEFAULT_DIRECTION
    context['shop_sort_direction'] = shop_sort_direction

    if 'shop_show_count' in request.session:
        context['shop_show_count'] = request.session['shop_show_count']
    else:
        context['shop_show_count'] = settings.SHOP_SHOW_COUNT_DEFAULT
    context['shop_show_counts'] = settings.SHOP_SHOW_COUNT

    query = context['goods'].paginator.object_list
    if query.aggregate(Max('priceinshop__price_card'))['priceinshop__price_card__max']:
        context['price_max'] = query.aggregate(Max('priceinshop__price_card'))['priceinshop__price_card__max']
    else:
        context['price_max'] = 10000
    if query.aggregate(Min('priceinshop__price_card'))['priceinshop__price_card__min']:
        context['price_min'] = query.aggregate(Min('priceinshop__price_card'))['priceinshop__price_card__min']
    else:
        context['price_min'] = 0
    if context['price_max'] == context['price_min']:
        context['price_min'] = 0

    brands = list(query.order_by('brand__name').values_list('brand__name', 'brand__id').
                  annotate(bcount=Count('brand__id')).filter(brand__isnull=False))
    brands_d = []
    for i in brands:
        i += (False, )
        brands_d.append(i)
    context['brands'] = brands_d

    if properties:
        ids = query.values_list('id', flat=True)
        gp = list(GoodProperty.objects.filter(good__in=ids).
                  filter(property__is_public=True, is_public=True).
                  values('value', 'property__name', 'property__id').
                  annotate(g_count=Count('good_id')))

        properties = get_properties(gp)
        context['properties'] = properties
    else:
        context['properties'] = []

    if 'q' in request.GET and request.GET['q']:
        context['shop_search_q'] = request.GET['q']
    else:
        context['shop_search_q'] = ''

    c = query.order_by('category__name').values_list(
        'category__name', 'category__id', 'category__order', 'category__parent__name', 'category__parent__id',
        'category__parent__order', 'category__parent__parent__name', 'category__parent__parent__id',
        'category__parent__parent__order').\
        annotate(bcount=Count('category__id')).filter(category__isnull=False)

    get_cats = request.GET.getlist('categories[]')

    shop_categories = ''

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

    categories = categories_sum(categories)

    categories_2 = []
    level1_cat = None
    if len(categories) == 1:
        categories[0]['checked'] = True
        level1_cat = categories[0]['id']
        shop_categories = mark_safe("'%s'" % level1_cat)
        c = query.filter(Q(category__parent__id=level1_cat) | Q(category__parent__parent__id=level1_cat)). \
            order_by('category__name').values_list(
            'category__name', 'category__id', 'category__order', 'category__parent__name', 'category__parent__id',
            'category__parent__order', 'category__parent__parent__name'). \
            annotate(bcount=Count('category__id')).filter(category__isnull=False)
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
            categories_2.append({
                'name': c_name, 'id': c_id, 'count': i[7], 'order': c_order, 'checked': str(c_id) in get_cats
            })
        categories_2 = categories_sum(categories_2)
        context['categories_filter_2'] = categories_2

    if len(categories) == 1 and len(categories_2) == 1:
        categories_2[0]['checked'] = True
        level2_cat = categories_2[0]['id']
        shop_categories = mark_safe("'%s', '%s'" % (level1_cat, level2_cat))
        categories_3 = []
        c = query.filter(Q(category__parent__id=level2_cat)). \
            order_by('category__name').values_list(
            'category__name', 'category__id', 'category__order'). \
            annotate(bcount=Count('category__id')).filter(category__isnull=False)
        for i in c:
            categories_3.append({
                'name': i[0], 'id': i[1], 'count': i[3], 'order': i[2], 'checked': str(i[1]) in get_cats
            })
        context['categories_filter_3'] = categories_sum(categories_3)

    context['categories_filter'] = categories
    context['shop_categories'] = shop_categories

    return context


def categories_sum(categories):

    new_cats = []
    for i in categories:

        cat_exists = False

        for c in new_cats:
            if c['id'] == i['id']:
                cat_exists = True
                c['count'] += i['count']

        if not cat_exists:
            new_cats.append(i)

    return sorted(new_cats, key=lambda k: k['order'])


def get_properties(gp):

    properties = []
    for i in gp:
        p_item = None
        for p in properties:
            if p['name'] == i['property__name']:
                p_item = p
        if p_item is None:
            properties.append({'name': i['property__name'], 'id': i['property__id'], 'lock': False, 'items': [{
                'count': i['g_count'],
                'value': i['value'],
                'id': i['property__id'],
            }]})
        else:
            p_item['items'].append({'count': i['g_count'], 'value': i['value'], 'checked': False})

    return properties
