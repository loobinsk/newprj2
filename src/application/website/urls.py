from django.conf.urls import url

from pages.views import PageView

app_name = 'website'
urlpatterns = [
    url('^$', PageView.as_view()),
]
