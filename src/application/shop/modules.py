from pages.registry import modules, Module
from django.utils.translation import ugettext as _


@modules.register
class Sale(Module):
    name = _('Sale')
    url_name = 'shop:sale'


@modules.register
class New(Module):
    name = _('New')
    url_name = 'shop:new'


@modules.register
class Search(Module):
    name = _('Search')
    url_name = 'shop:search'


@modules.register
class Registration(Module):
    name = _('Registration')
    url_name = 'shop:registration'


@modules.register
class Login(Module):
    name = _('Login')
    url_name = 'shop:login'


@modules.register
class Personal(Module):
    name = _('Personal area')
    url_name = 'shop:personal'


@modules.register
class Cart(Module):
    name = _('Cart')
    url_name = 'shop:cart'


@modules.register
class RestorePassword(Module):
    name = _('Restore password')
    url_name = 'shop:restore_password'


@modules.register
class Checkout(Module):
    name = _('Checkout')
    url_name = 'shop:checkout'
