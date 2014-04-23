from django.conf.urls import patterns, url
import django_cas
from account import views


#url(regex and form action and website url, views.py name, nothing)
#url(nicole and laura, laura, laura)
urlpatterns = patterns('',
    url(r'^$', views.account_index, name='account_index'),
    url(r'profile/$', views.profile, name='profile'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', django_cas.views.logout, name='logout'),
    url(r'^remove/$', views.account_index, name='remove_offer'),
    url(r'^unfollow/$', views.account_index, name='unfollow'),
)
