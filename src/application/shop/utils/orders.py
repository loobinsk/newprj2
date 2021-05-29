import datetime

from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from preferences.utils import get_setting

from ..models import Order, OrderGood, Good, User
from ..tasks import send_mail_html, send_sms


def prepare_order_data(order, required_fields):
    prepared_order = {}
    if order:
        for origin, dest in required_fields.items():
            dest_data = getattr(order, origin)
            if not dest_data or dest_data == 'None':
                dest_data = '-'
            prepared_order[dest] = dest_data
    return prepared_order


def get_user_orders(user):
    orders = Order.objects.filter(user=user)
    return orders


def get_order_goods(user, order):
    order = get_object_or_404(Order, user=user, pk=str(order))
    order_goods = OrderGood.objects.filter(order=order)

    return order, order_goods


def save_order(cart, data, user, new_user=False):

    purchase_goods = []
    order_goods = []

    user_mail = None

    for i in cart.cart:
        if i['is_order']:
            order_goods.append(i)
        else:
            purchase_goods.append(i)

    ids = []

    purchase_goods_c = []

    if purchase_goods:
        order_obj = Order()
        if user:
            user_mail = user.email
            order_obj.user = user
        order_obj.payment = str(data['payment'])
        order_obj.delivery = "Самовывоз ({})".format(str(data['delivery']))
        order_obj.city = data['delivery'].region.region_name
        order_obj.street = data['street']
        order_obj.house = data['house']
        order_obj.apartment = data['apartment']
        order_obj.name = data['name']
        order_obj.phone = data['phone']
        order_obj.type = 0
        order_obj.save()
        ids.append(str(order_obj.id))

        count = 0
        sum_a = 0
        for i in purchase_goods:
            og_obj = OrderGood()
            og_obj.order = order_obj
            og_obj.name = i['name']
            og_obj.vendor_code = i['vendor_code']
            og_obj.url = i['url']
            og_obj.price = i['price']
            og_obj.price_card = i['price']
            og_obj.count = i['count']
            og_obj.image = i['image']

            count += og_obj.count
            sum_a += og_obj.count * og_obj.price_card

            purchase_goods_c.append({
                'vendor_code': i['vendor_code'],
                'name': i['name'],
                'price': i['price'],
                'count': i['count'],
                'sum': i['price'] * i['count'],
                'url': i['url'][1:]
            })

            try:
                good_obj = Good.objects.get(id=i['id'])
                og_obj.good = good_obj
            except Good.DoesNotExist:
                pass

            og_obj.save()

        order_obj.count = count
        order_obj.sum = sum_a
        order_obj.save()

    order_goods_c = []

    if order_goods:
        order_obj = Order()
        if user:
            user_mail = user.email
            order_obj.user = user
        order_obj.payment = str(data['payment'])
        order_obj.delivery = str(data['delivery'])
        order_obj.city = data['city']
        order_obj.street = data['street']
        order_obj.house = data['house']
        order_obj.apartment = data['apartment']
        order_obj.name = data['name']
        order_obj.phone = data['phone']
        order_obj.type = 1
        order_obj.save()

        ids.append(str(order_obj.id))

        count = 0
        sum_a = 0
        for i in order_goods:
            og_obj = OrderGood()
            og_obj.order = order_obj
            og_obj.name = i['name']
            og_obj.vendor_code = i['vendor_code']
            og_obj.url = i['url']
            og_obj.price = i['price']
            og_obj.price_card = i['price']
            og_obj.count = i['count']
            og_obj.image = i['image']

            count += og_obj.count
            sum_a += og_obj.count * og_obj.price_card

            order_goods_c.append({
                'vendor_code': i['vendor_code'],
                'name': i['name'],
                'price': i['price'],
                'count': i['count'],
                'sum': i['price'] * i['count'],
                'url': i['url'][1:]
            })

            try:
                good_obj = Good.objects.get(id=i['id'])
                og_obj.good = good_obj
            except Good.DoesNotExist:
                pass

            og_obj.save()

        order_obj.count = count
        order_obj.sum = sum_a
        order_obj.save()

    email_of_shop = data['delivery'].email

    send_mail_html(
        name='order',
        to_email=email_of_shop,
        subject=_('Issued order number %s on the website') % ','.join(ids),
        context={
            'date': datetime.datetime.now().strftime('%d.%m.%Y %H:%M'),
            'name': data['name'],
            'phone': data['phone'],
            'purchase_goods': purchase_goods_c,
            'order_goods': order_goods_c,
            'order_goods_sum': cart.sum_order,
            'purchase_goods_sum': cart.sum_purchase
        }
    )

    if user_mail:
        send_mail_html(
            name='order_user',
            to_email=user_mail,
            subject=_('Order No %s on the MANDARIN website') % ','.join(ids),
            context={
                'date': datetime.datetime.now().strftime('%d.%m.%Y %H:%M'),
                'name': data['name'],
                'phone': data['phone'],
                'purchase_goods': purchase_goods_c,
                'order_goods': order_goods_c,
                'id': ','.join(ids),
                'order_goods_sum': cart.sum_order,
                'purchase_goods_sum': cart.sum_purchase
            }
        )

    send_sms.delay(data['phone'], str(_('Thank you! Your order number %s accepted. '
                                        'We will contact you shortly. MANDARIN') % ','.join(ids)))
    if new_user:
        generated_password = User.objects.make_random_password()
        user.set_password(generated_password)
        user.save()

        send_sms.delay(
            data['phone'],
            str(_('Thank for registration! Yor credentials login: %(phone)s password: %(password)s '
                  'You can change this data on your account page.') % {'phone': data['phone'],
                                                                       'password': generated_password}))
