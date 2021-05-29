from django.utils.translation import ugettext_lazy as _

from ..models import Good

from preferences.utils import get_setting


class Cart:
    def __init__(self, request):
        self.request = request
        self.cart = self.request.session.get('cart', [])

    def add(self, good_id, count):

        try:
            good = Good.objects.get(id=good_id, is_public=True)
        except (Good.DoesNotExist, ValueError):
            raise Exception(_('Error. Bad product.'))

        if not count:
            count = 1

        try:
            count = int(count)
            if count < 1:
                count = 1
        except ValueError:
            raise Exception('Error. Bad products count.')

        # if not self.request.user or not self.request.user.is_authenticated:
        #     raise Exception('Error. User not authorized.')

        cart_item = self.get(good_id)
        if cart_item:
            cart_item['count'] += count
            cart_item['sum'] = cart_item['count'] * cart_item['price']
        else:
            region = self.request.user.region if self.request.user.is_authenticated else self.request.session.get('region')
            price = good.get_price_card_for_region(region)
            good_sum = price * count
            image = ''
            if good.image:
                image = good.image.path
            self.cart.append({'id': good_id, 'count': count, 'name': str(good), 'url': good.get_absolute_url(),
                              'price': price, 'sum': good_sum, 'image': image, 'vendor_code': good.vendor_code,
                              'available': good.count, 'is_order': good.is_order})
        self.calc()
        self.save()

    def save(self):
        self.request.session['cart'] = self.cart

    def get(self, good_id):
        for item in self.cart:
            if item['id'] == good_id:
                return item
        return None

    def edit(self, good_id, count):

        cart_item = self.get(good_id)

        if not cart_item:
            raise Exception(_('Bad cart item'))
        if not count:
            count = 1

        try:
            count = int(count)
            if count < 1:
                count = 1
        except ValueError:
            raise Exception('Error. Bad products count.')

        cart_item['count'] = count
        cart_item['sum'] = cart_item['count'] * cart_item['price']
        self.calc()
        self.save()

    def delete(self, good_id):
        cart_item = self.get(good_id)
        if not cart_item:
            raise Exception(_('Bad cart item'))

        self.cart.remove(cart_item)
        self.save()

    def clear(self):
        self.cart = []
        self.save()

    def calc(self):
        for item in self.cart:

            good = Good.objects.get(id=item['id'])
            region = self.request.user.region if self.request.user.is_authenticated else self.request.session.get('region')
            item['price'] = good.get_price_card_for_region(region)
            item['sum'] = item['price'] * item['count']

    @property
    def sum(self):
        s = 0
        for item in self.cart:
            s += item['sum']
        return s

    @property
    def sum_purchase(self):
        s = 0
        for item in self.purchase_goods:
            s += item['sum']
        return s

    @property
    def sum_order(self):
        s = 0
        for item in self.order_goods:
            s += item['sum']
        return s

    @property
    def count(self):
        c = 0
        for item in self.cart:
            c += item['count']
        return c

    @property
    def count_purchase(self):
        c = 0
        for item in self.purchase_goods:
            c += item['count']
        return c

    @property
    def count_order(self):
        c = 0
        for item in self.order_goods:
            c += item['count']
        return c

    @property
    def is_diff(self):
        have_is_order = False
        have_not_is_order = False
        for item in self.cart:
            if item['is_order']:
                have_is_order = True
            if not item['is_order']:
                have_not_is_order = True
        return have_is_order and have_not_is_order

    @property
    def order_goods(self):
        data = []
        for item in self.cart:
            if item['is_order']:
                data.append(item)
        return data

    @property
    def purchase_goods(self):
        data = []
        for item in self.cart:
            if not item['is_order']:
                data.append(item)
        return data
