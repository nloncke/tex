from django.conf.urls import patterns, url

from account import views

#url(regex and form action and website url, views.py name, nothing)
#url(nicole and laura, laura, laura)
urlpatterns = patterns('',
    url(r'^$', views.account_index, name='account_index'),
)
