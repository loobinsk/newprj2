import re

from django.views.generic import DetailView, TemplateView

from pages.models import PageModule
from pages.views import ModuleViewMixin


from ..models import Brand, Good
from ..utils import get_goods, goods_context


class AjaxSearchView(TemplateView):
    template_name = 'shop/ajax_search.html'
    goods = None
    q = ''

    def get_context_data(self, **kwargs):

        context = super(AjaxSearchView, self).get_context_data(**kwargs)
        context['q'] = self.q
        a_q = context['q'].split(' ')
        for i in self.goods.object_list:
            name = i.name
            title = i.title
            vendor_code = i.vendor_code

            for j in a_q:
                if len(j) > 1:
                    repl = re.compile(re.escape(j), re.IGNORECASE)
                    name = repl.sub('<span class="active">%s</span>' % j, name)
                    title = repl.sub('<span class="active">%s</span>' % j, title)
                    vendor_code = repl.sub('<span class="active">%s</span>' % j, vendor_code)
            i.name = name
            i.title = title
            i.vendor_code = vendor_code
        context['goods'] = self.goods
        region = self.request.user.region if self.request.user.is_authenticated else self.request.session.get('region')
        for good in self.goods:
            good.price_card = good.get_price_card_for_region(region)
        return context

    def get(self, request, *args, **kwargs):
        search_q = self.request.GET.get('q', '')
        self.q = search_q
        self.goods = get_goods(self.request, page_count=8)
        return super(AjaxSearchView, self).get(request, *args, **kwargs)


class BrandAjaxView(DetailView):

    model = Brand
    template_name = 'shop/ajax_brand.html'

    def get_context_data(self, **kwargs):

        context = super(BrandAjaxView, self).get_context_data(**kwargs)

        # Goods
        goods = Good.objects.filter(brand=self.object, is_public=True)
        context['goods'] = goods

        return context


class SearchView(ModuleViewMixin, TemplateView):

    template_name = 'shop/catalog.html'
    module = 'shop_search'

    def get_context_data(self, **kwargs):

        # History
        self.history = [PageModule.assign(self.module).history_item]

        context = super(SearchView, self).get_context_data(**kwargs)

        # Goods
        goods = get_goods(self.request)
        context['goods'] = goods
        context = goods_context(self.request, context, False)

        return context
