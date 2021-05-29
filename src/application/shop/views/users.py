from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView, UpdateView

from ajax.decorators import ajax_view
from pages.views import ModuleViewMixin
from preferences.utils import get_setting

from ..decorators import anonymous_required
from ..forms import RegistrationForm, LoginForm, UserForm, RestorePasswordForm
from ..models import User
from ..tasks.mail import send_mail
from ..utils import sms, get_user_orders, prepare_order_data


@ajax_view
class RegistrationView(ModuleViewMixin, FormView):

    module = 'shop_registration'
    form_class = RegistrationForm
    template_name = ''
    success_url = '/'

    @method_decorator(anonymous_required)
    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        if form.cleaned_data['email']:
            send_mail.delay(
                name='registration',
                to_email=form.cleaned_data['email'],
                subject=_('Registration on site %s') % get_setting('website_sitename', ''),
                context={'name': form.cleaned_data['name'], 'email': form.cleaned_data['email'],
                         'phone': form.cleaned_data['phone'], 'password': form.cleaned_data['password']}
            )
        login(self.request, user)
        return super(RegistrationView, self).form_valid(form)


@ajax_view
class RestorePasswordView(ModuleViewMixin, FormView):
    module = 'shop_restorepassword'
    form_class = RestorePasswordForm
    template_name = ''

    @method_decorator(anonymous_required)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(RestorePasswordView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.user
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()

        if form.is_phone:
            sms.send_message(user.phone, 'Новый пароль: {}'.format(password))
        else:
            user.set_password(password)
            user.save()
            send_mail.delay(
                name='restore_password',
                to_email=user.email,
                subject='Новый пароль %s' % get_setting('website_sitename', ''),
                context={'password': password}
            )
        return super(RestorePasswordView, self).form_valid(form)


@ajax_view
class LoginView(ModuleViewMixin, FormView):

    module = 'shop_login'
    form_class = LoginForm
    template_name = ''
    success_url = '/'

    @method_decorator(anonymous_required)
    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):

    url = '/'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).dispatch(request, *args, **kwargs)


@ajax_view
class PersonalView(ModuleViewMixin, UpdateView):

    module = 'shop_personal'
    form_class = UserForm
    model = User

    @method_decorator(login_required(login_url='/'))
    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(PersonalView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PersonalView, self).get_context_data(**kwargs)
        orders = get_user_orders(self.request.user)
        required_fields = {
            'id': 'order_number',
            'date_create': 'date',
            'payment': 'payment',
            'delivery': 'delivery',
            'order_type': 'type',
            'sum': 'total_price',
            'count': 'total_goods'

        }
        context['orders'] = [
            prepare_order_data(order, required_fields) for order in orders
        ]
        return context

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        if form.cleaned_data.get('confirm_password'):
            password = form.cleaned_data.get('confirm_password')
            if form.cleaned_data.get('email'):
                send_mail.delay(
                    name='restore_password',
                    to_email=form.cleaned_data.get('email'),
                    subject='Новый пароль %s' %
                            get_setting('website_sitename', ''),
                    context={'password': password}
                )
            else:
                sms.send_message(form.cleaned_data.get('phone'),
                                 'Новый пароль: {}'.format(password))

        login(self.request, self.get_object())
        return super(PersonalView, self).form_valid(form)
