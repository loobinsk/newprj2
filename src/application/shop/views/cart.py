from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.generic import View, TemplateView, FormView

from ajax.decorators import ajax_view
from pages.views import ModuleViewMixin

from ..classes import Cart
from ..forms import CheckoutForm
from ..models import Delivery
from ..utils import save_order, get_or_create_user_from_order


class AjaxCartAddView(View):

    def get(self, request):

        good_id = request.GET.get('id')
        count = request.GET.get('count')

        cart = Cart(request)

        try:
            cart.add(good_id, count)
        except Exception as e:
            return HttpResponse(str(e), content_type='text/plain')

        return HttpResponse(_('Good added to cart.'), content_type='text/plain')


class AjaxCartEditView(View):

    def get(self, request):

        good_id = request.GET.get('id')
        count = request.GET.get('count')

        cart = Cart(request)

        try:
            cart.edit(good_id, count)
        except Exception as e:
            return HttpResponse(str(e), content_type='text/plain')

        return HttpResponse(_('Good cart edited.'), content_type='text/plain')


class AjaxCartInfoView(View):

    def get(self, request):
        cart = Cart(request)
        return HttpResponse("{}|{}".format(cart.count, cart.sum), content_type='text/plain')


class AjaxCartDeleteView(View):

    def get(self, request):

        good_id = request.GET.get('id')
        cart = Cart(request)

        try:
            cart.delete(good_id)
        except Exception as e:
            return HttpResponse(str(e), content_type='text/plain')

        return HttpResponse(_('Good deleted from cart.'), content_type='text/plain')


class AjaxCartView(TemplateView):

    template_name = 'shop/ajax_cart.html'

    def get_context_data(self, **kwargs):
        context = super(AjaxCartView, self).get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart'] = cart
        return context


class CartView(ModuleViewMixin, TemplateView):

    template_name = 'shop/cart.html'
    module = 'shop_cart'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(CartView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        cart = Cart(self.request)

        context['cart'] = cart
        return context


@ajax_view
class CheckoutView(ModuleViewMixin, FormView):

    template_name = 'shop/checkout.html'
    module = 'shop_checkout'
    form_class = CheckoutForm
    success_url = '/'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(CheckoutView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart'] = cart
        context['delivery'] = Delivery.objects.all()
        return context

    def form_valid(self, form):
        created = False
        if self.request.user.is_anonymous:
            self.request.user, created = get_or_create_user_from_order(form.cleaned_data)
        cart = Cart(self.request)
        save_order(cart, form.cleaned_data, self.request.user, created)
        cart.clear()
        return super(CheckoutView, self).form_valid(form)

    def get_initial(self):
        if self.request.user.is_authenticated:
            self.initial = {
                'name': self.request.user.name,
                'phone': self.request.user.phone,
            }
        return super(CheckoutView, self).get_initial()
