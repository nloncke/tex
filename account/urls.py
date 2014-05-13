from django.conf.urls import patterns, url
import django_cas
from account import views

urlpatterns = patterns('',
    url(r'^$', views.account_index, name='account_index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', django_cas.views.logout, name='logout'),
    url(r'^remove/$', views.account_index, name='remove_offer'),
    url(r'^unfollow/$', views.account_index, name='unfollow'),
)
