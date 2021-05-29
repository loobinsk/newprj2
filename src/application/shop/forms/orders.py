from ajax.forms import AjaxFormMixin
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

from ..models import Delivery, City, Payment, Shop, Region


class CheckoutForm(AjaxFormMixin, forms.Form):

    antispam_field = 'name'

    payment = forms.ModelChoiceField(
        queryset=Payment.objects.filter(is_public=True),
        label=_('Payment methods'),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None
    )

    delivery = forms.ModelChoiceField(
        queryset=Shop.objects.filter(is_public=True),
        label=_('Goods get'),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None
    )

    city = forms.ModelChoiceField(
        queryset=Region.objects.filter(is_public=True),
        label=_('City'),
        widget=forms.Select(attrs={
            'class': 'select__order',
        }),
        required=False,
        empty_label=None
    )
    street = forms.CharField(
        label=_('Street'),
        widget=forms.TextInput(attrs={
            'class': 'input__default',
            'placeholder': _('Street')
        }),
        required=False,
    )

    house = forms.CharField(
        label=_('House'),
        widget=forms.TextInput(attrs={
            'class': 'input__default',
            'placeholder': _('House')
        }),
        required=False,
    )

    apartment = forms.CharField(
        label=_('Apartment'),
        widget=forms.TextInput(attrs={
            'class': 'input__default',
            'placeholder': _('Apartment')
        }),
        required=False,
    )

    name = forms.CharField(
        label=_('Receiver name'),
        widget=forms.TextInput(attrs={
            'class': 'input__default',
            'placeholder': _('Receiver name')
        })
    )

    phone = forms.CharField(
        label=_('Phone'),
        widget=forms.TextInput(attrs={
            'class': 'input__default',
            'placeholder': _('Phone')
        }),
        validators=[
            RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message=_('Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.'))]
    )

    def __init__(self, *args, **kwargs):

        super(CheckoutForm, self).__init__(*args, **kwargs)
