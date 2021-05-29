from django.conf.urls import url, include

from . import views


patterns = ([

    # Users
    url(r'^registration/$', views.RegistrationView.as_view(), name='registration'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^restore_password/$', views.RestorePasswordView.as_view(), name='restore_password'),
    url(r'^personal/$', views.PersonalView.as_view(), name='personal'),

    # Brand
    url(r'^brand/(?P<slug>[\w-]+)/$',
        views.BrandDetailView.as_view(), name='brand'),

    # Sale and New
    url(r'^sale/$',
        views.SaleView.as_view(), name='sale'),
    url(r'^new/$',
        views.NewView.as_view(), name='new'),
    url(r'^search/$',
        views.SearchView.as_view(), name='search'),

    # Cart
    url(r'^cart/$', views.CartView.as_view(), name='cart'),
    url(r'^checkout/$', views.CheckoutView.as_view(), name='checkout'),

    # Order
    url(r'^order/$', views.OrderView.as_view(), name='new-order'),
    url(r'^order_detail/$', views.OrderDetailView.as_view(), name='order-detail'),

    # Ajax
    url(r'^ajax/good/(?P<pk>[\d]+)/$', views.GoodAjaxView.as_view(), name='good_ajax'),
    url(r'^ajax/brand/(?P<slug>[\w-]+)/$', views.BrandAjaxView.as_view(), name='brand_ajax'),
    url(r'^ajax/search/$', views.AjaxSearchView.as_view(), name='search_ajax'),

    # Goods
    url(r'^ajax/goods/$', views.GoodsAjaxView.as_view(), name='goods_ajax'),
    url(r'^ajax/filters/$', views.AjaxFiltersView.as_view(), name='filters_ajax'),
    url(r'^ajax/filters/brands/$', views.AjaxFiltersBrandsView.as_view(), name='filters_brands_ajax'),
    url(r'^ajax/filters/categories/$', views.AjaxFiltersCategoriesView.as_view(), name='filters_categories_ajax'),
    url(r'^ajax/filters/prices/$', views.AjaxFiltersPricesView.as_view(), name='filters_prices_ajax'),

    # Region
    url(r'^ajax/choose-region/', views.ChooseRegionView.as_view(), name='choose_region_ajax'),

    # Good
    url(r'^(?P<category_1>[\w-]+)/(?P<category_2>[\w-]+)/(?P<category_3>[\w-]+)/g-(?P<slug>[\w-]+)/$',
        views.GoodDetailView.as_view(), name='good'),
    url(r'^(?P<category_1>[\w-]+)/(?P<category_2>[\w-]+)/g-(?P<slug>[\w-]+)/$',
        views.GoodDetailView.as_view(), name='good'),
    url(r'^(?P<category_1>[\w-]+)/g-(?P<slug>[\w-]+)/$',
        views.GoodDetailView.as_view(), name='good'),

    # Category
    url(r'^(?P<category_1>[\w-]+)/$',
        views.CategoryDetailView.as_view(), name='category'),
    url(r'^(?P<category_1>[\w-]+)/(?P<category_2>[\w-]+)/$',
        views.CategoryDetailView.as_view(), name='category'),
    url(r'^(?P<category_1>[\w-]+)/(?P<category_2>[\w-]+)/(?P<category_3>[\w-]+)/$',
        views.CategoryDetailView.as_view(), name='category'),

], 'shop')

# Cart
cart_patterns = ([

    url(r'^$', views.AjaxCartView.as_view(), name='cart'),
    url(r'^info/$', views.AjaxCartInfoView.as_view(), name='info'),
    url(r'^add/$', views.AjaxCartAddView.as_view(), name='add'),
    url(r'^edit/$', views.AjaxCartEditView.as_view(), name='edit'),
    url(r'^delete/$', views.AjaxCartDeleteView.as_view(), name='delete'),

], 'shop-cart')

# All patterns
urlpatterns = [

    url(r'^ajax/cart/', include(cart_patterns)),
    url(r'^', include(patterns)),

]

