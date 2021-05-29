from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cache_model.models import CacheModel
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from pages.models import CustomPage
from public_model.models import PublicModel
from sorl.thumbnail import ImageField
from sort_model.models import OrderModel


class Category(MPTTModel, CacheModel, OrderModel, PublicModel, CustomPage):

    SUBMENU_DIRECTIONS = (
        ('left', _('Left')),
        ('right', _('Right')),
    )

    name = models.CharField(_('Name'), max_length=150)
    slug = models.SlugField(_('System name'), max_length=100)
    parent = TreeForeignKey('self', verbose_name=_('Parent'), null=True, blank=True)
    content_bottom = RichTextField(_('Content bottom'), blank=True)

    submenu_direction = models.CharField(_('Submenu direction'), choices=SUBMENU_DIRECTIONS, default='left',
                                         max_length=5)

    image = ImageField(_('Image'), upload_to='shop/categories/', blank=True)

    url = models.CharField(max_length=400, blank=True, editable=False)

    objects = models.Manager()

    class Meta:
        db_table = 'shop_category'
        ordering = ['tree_id', 'lft']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        unique_together = (('parent', 'slug'), ('parent', 'name'))

    class MPTTMeta:
        order_insertion_by = ['order']

    class CacheMeta:
        cache_fields = [('parent_id', 'parent.id'), ('parent_parent_id', 'parent.parent.id')]

    def get_absolute_url(self):
        if self.parent is None:
            return reverse('shop:category', args=[str(self.slug)])
        if self.parent is not None and self.parent.parent is None:
            return reverse('shop:category', args=[str(self.parent.slug), str(self.slug)])
        else:
            return reverse('shop:category', args=[str(self.parent.parent.slug), str(self.parent.slug), str(self.slug)])

    def save(self, *args, **kwargs):
        self.url = self.get_absolute_url()
        super(Category, self).save(*args, **kwargs)


class Brand(CacheModel, PublicModel, CustomPage):

    name = models.CharField(_('Name'), max_length=100, unique=True)
    slug = models.SlugField(_('System name'), max_length=100, unique=True)
    image = ImageField(_('Image'), upload_to='shop/brands/', blank=True)

    is_popular = models.BooleanField(_('Is popular'), default=False, blank=True)

    objects = models.Manager()

    class Meta:
        db_table = 'shop_brand'
        ordering = ['name']
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')

    def __str__(self):
        return '%s' % self.name

    def get_absolute_url(self):
        return reverse('shop:brand', args=[str(self.slug)])
