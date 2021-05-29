from datetime import datetime

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import models as django_auth_models
from public_model.models import ActiveModel

from .regions import Region


class UserManager(django_auth_models.BaseUserManager):

    def create_user(self, phone, password=None):

        if not phone:
            raise ValueError(_('Users must have phone'))

        user = self.model(
            phone=phone,
        )

        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password):

        user = self.create_user(phone, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(ActiveModel, django_auth_models.PermissionsMixin, django_auth_models.AbstractBaseUser):

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_('Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.')
    )
    phone = models.CharField(_('Phone'), max_length=17, unique=True, validators=[phone_regex])

    email = models.EmailField(_('E-mail'), max_length=75, unique=True, null=True)
    name = models.CharField(_('User name'), max_length=100, default='', blank=True)

    is_staff = models.BooleanField(_('Is staff'), default=False)

    date_joined = models.DateField(_('Date created'), default=datetime.now)

    region = models.ForeignKey(Region, blank=True, null=True, on_delete=models.SET_NULL)

    objects = UserManager()

    USERNAME_FIELD = 'phone'

    class Meta:
        db_table = 'auth_user'
        ordering = ['phone']
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def get_full_name(self):
        return self.phone

    def get_short_name(self):
        return self.phone

    def get_default_region(self):
        try:
            default_region = Region.objects.get(default_region=True)
        except:
            default_region = None

        return default_region

    def __str__(self):
        return self.phone


class CustomAnonymousUser(django_auth_models.AnonymousUser):

    def get_default_region(self):
        try:
            default_region = Region.objects.get(default_region=True)
        except:
            default_region = None

        return default_region

    def get_default_shop(self):
        try:
            default_region = Region.objects.get(default_region=True)
        except:
            default_region = None

        return default_region


django_auth_models.AnonymousUser = CustomAnonymousUser
