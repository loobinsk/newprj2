from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AdminPasswordChangeForm
from django.utils.translation import ugettext_lazy as _

from public_model.admin import active_model
from preferences.utils import get_setting

from ..models import User
from ..tasks.mail import send_mail
from ..utils import sms


class MyAdminPasswordChangeForm(AdminPasswordChangeForm):
    def save(self, commit=True):
        password = self.cleaned_data["password1"]

        if self.user.email:
            send_mail.delay(
                name='restore_password',
                to_email=self.user.email,
                subject='Новый пароль %s' % get_setting('website_sitename', ''),
                context={'password': password}
            )
        else:
            sms.send_message(self.user.phone, 'Новый пароль: {}'.format(password))

        super(MyAdminPasswordChangeForm, self).save(commit=commit)


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone', )

    def clean_password2(self):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))

        return password2

    def save(self, commit=True):

        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
             "Raw passwords are not stored, so there is no way to see "
             "this user's password, but you can change the password "
             "using <a href=\"../password/\">this form</a>.")
    )

    class Meta:
        model = User
        fields = "__all__"

    def clean_password(self):
        return self.initial["password"]


@active_model
class UserAdmin(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = MyAdminPasswordChangeForm

    list_display = ('phone', 'name', 'email', 'date_joined', 'last_login', 'is_staff', 'is_superuser', )

    fieldsets = (
        (None, {
            'fields': ('phone', 'password')
        }),
        (_('Personal data'), {
            'fields': ('name', 'email', 'region')
        }),
        (_('Permissions'), {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions', )
        }),
        (_('Important dates'), {
            'fields': ('date_joined', 'last_login',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', )
        }),
    )

    search_fields = ('phone', 'name', 'email', )
    filter_horizontal = ('groups', 'user_permissions', )
    list_filter = ('is_staff', 'is_superuser', )
    readonly_fields = ('date_joined', )
    list_per_page = 40
    ordering = ('phone',)


admin.site.register(User, UserAdmin)
