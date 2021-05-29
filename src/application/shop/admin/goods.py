from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.forms.models import BaseInlineFormSet

from seo.admin import seo_model
from sort_model.admin import order_model_inline
from public_model.admin import public_model
from mptt.forms import TreeNodeChoiceField

from ..models import Category, Good, GoodImage, GoodProperty, PriceInShop


@order_model_inline
class GoodImageInlineTabularAdmin (admin.TabularInline):
    model = GoodImage
    fields = ('name', 'image', 'is_public', )
    extra = 0


class GoodPropertyInlineTabularAdmin (admin.TabularInline):
    model = GoodProperty
    fields = ('property', 'value', 'is_public', )
    raw_id_fields = ('property', )
    extra = 0


class PriceInShopTabularInlineFormset(BaseInlineFormSet):
    def save_new(self, form, commit=True):
        return super(PriceInShopTabularInlineFormset, self).save_new(form, commit=commit)

    def save_existing(self, form, instance, commit=True):
        return form.save(commit=commit)


class GoodPriceInShopTabularAdmin(admin.TabularInline):
    model = PriceInShop
    fields = ('shop', 'price', 'price_card', 'count', 'is_order', 'is_sale', 'is_new', 'is_hit')
    extra = 0
    formset = PriceInShopTabularInlineFormset


class GoodAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GoodAdminForm, self).__init__(*args, **kwargs)
        self.fields['category'] = TreeNodeChoiceField(label=self.fields['category'].label, queryset=Category.objects.all())

    class Meta:
        model = Good
        exclude = []


@seo_model
@public_model
@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):

    list_display = ('name',  'vendor_code', 'category', 'brand', 'price', 'price_card', 'count', 'is_sale',
                    'is_new', 'is_hit', 'is_order')
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': (('name', 'title'), 'slug', 'vendor_code', )
        }),

        (_('Categories'), {
            'fields': ('category', 'brand')
        }),
        (_('Price and count'), {
            'fields': ('price', 'price_card', 'count')
        }),
        (_('Data'), {
            'fields': ('image', 'content')
        }),
        (_('Flags'), {
            'fields': ('is_sale', 'is_new', 'is_hit', )
        }),
    )
    search_fields = ['name', 'title', 'slug', 'vendor_code', 'category__name', 'brand__name', 'content']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_sale', 'is_new', 'is_hit', 'is_order', 'brand')
    list_per_page = 40
    readonly_fields = ('count', )
    list_select_related = ('brand', 'category')
    inlines = [GoodImageInlineTabularAdmin, GoodPropertyInlineTabularAdmin, GoodPriceInShopTabularAdmin]
    form = GoodAdminForm

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
            instance.good.update_count()
        formset.save_m2m()
