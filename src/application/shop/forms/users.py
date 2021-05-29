from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from ajax.forms import AjaxFormMixin

from ..models import User


class RegistrationForm(AjaxFormMixin, forms.ModelForm):

    antispam_field = 'phone'
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': _('Confirm password'), 'class': 'input__default'}))
    privacy = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'hidden'}
    ), required=False)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['phone'].required = True
        self.fields['name'].required = True
        self.fields['email'].required = False
        self.fields['password'].required = False

    class Meta:
        model = User
        fields = ('phone', 'name', 'email', 'password', 'confirm_password')

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('User name'), 'class': 'input__default'}),
            'phone': forms.TextInput(attrs={'placeholder': '+79999999999', 'class': 'input__default'}),
            'email': forms.TextInput(attrs={'placeholder': 'E-mail', 'class': 'input__default'}),
            'password': forms.PasswordInput(attrs={'placeholder': _('Create a password'), 'class': 'input__default'}),
        }

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                {'confirm_password': [_('The passwords you entered do not match'), ]}
            )

        if not cleaned_data.get('privacy'):
            raise forms.ValidationError(
                {'privacy': [
                    'Для продолжения регистрации нужно дать согласие'
                ]}
            )


class LoginForm(AjaxFormMixin, AuthenticationForm):

    antispam_field = 'phone'

    def __init__(self, *args, **kwargs):

        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': '+79999999999', 'class': 'input__default'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': _('Password'), 'class': 'input__default'
        })


class UserForm(AjaxFormMixin, forms.ModelForm):

    antispam_field = 'phone'

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input__default'}))

    class Meta:
        model = User
        fields = ('phone', 'name', 'email', 'password', 'confirm_password')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'input__default'}),
            'phone': forms.TextInput(attrs={'placeholder': '+79999999999', 'class': 'input__default'}),
            'email': forms.TextInput(attrs={'class': 'input__default'}),
            'password': forms.PasswordInput(attrs={'class': 'input__default'}),
        }

    def __init__(self, *args, **kwargs):

        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = False
        self.fields['password'].required = False
        self.fields['confirm_password'].required = False

    def clean(self):
        cleaned_data = super(UserForm, self).clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                {'confirm_password': [_('The passwords you entered do not match'), ]}
            )

        if cleaned_data.get('password'):
            self.instance.set_password(cleaned_data.get('password'))
        else:
            cleaned_data.pop('confirm_password', None)

        cleaned_data.pop('password', None)


class OrderForm(AjaxFormMixin, forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': _('Confirm password'),
                                          'class': 'input__default'}))
    privacy = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'hidden'}
    ), required=False)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['phone'].required = True
        self.fields['name'].required = True
        self.fields['password'].required = False

    class Meta:
        model = User
        fields = ('phone', 'name', 'password')

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('User name'), 'class': 'input__default'}),
            'phone': forms.TextInput(attrs={'placeholder': '+79999999999', 'class': 'input__default'}),
            'password': forms.PasswordInput(attrs={'placeholder': _('Create a password'), 'class': 'input__default'}),
        }

    def clean(self):
        cleaned_data = super(OrderForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                {'confirm_password': [_('The passwords you entered do not match'), ]}
            )

        if not cleaned_data.get('privacy'):
            raise forms.ValidationError(
                {'privacy': [
                    'Для продолжения регистрации нужно дать согласие'
                ]}
            )


class RestorePasswordForm(AjaxFormMixin, forms.Form):
    phone_or_email = forms.CharField(
        max_length=40, required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '+79999999999 или E-mail',
            'class': 'input__default'
        })
    )

    def __init__(self, *args, **kwargs):
        super(RestorePasswordForm, self).__init__(*args, **kwargs)

        self.user = None
        self.is_phone = False

    def clean(self):
        cleaned_data = super(RestorePasswordForm, self).clean()

        phone_or_email = cleaned_data.get('phone_or_email')

        self.user = User.objects.filter(phone=phone_or_email).first()

        if not self.user:
            self.user = User.objects.filter(email=phone_or_email).first()

            if not self.user:
                raise forms.ValidationError(
                    {'phone_or_email': ['Пользователь не найден']}
                )
        else:
            self.is_phone = True
