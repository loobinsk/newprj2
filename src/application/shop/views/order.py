from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import FormView, TemplateView
from ajax.decorators import ajax_view
from pages.views import ModuleViewMixin

from ..forms import OrderForm
from ..utils import get_order_goods


@ajax_view
class OrderView(ModuleViewMixin, FormView):

    module = 'shop_order'
    form_class = OrderForm
    template_name = ''
    success_url = '/shop/success/'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(OrderView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # cart = Cart(self.request)

        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        # order = order_new(form.cleaned_data, self.request.user, cart)

        login(self.request, user)
        return super(OrderView, self).form_valid(form)


class OrderDetailView(TemplateView):

    template_name = 'shop/order_detail.html'
    goods = []

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(OrderDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super(OrderDetailView, self).get_context_data(**kwargs)
        order = self.request.GET.get('order')
        if self.request.user.is_authenticated and order:
            user = self.request.user
            # Goods
            context['order'], context['order_goods'] = get_order_goods(
                user, order
            )
        return context
