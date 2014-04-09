from django.conf.urls import patterns, url

from sell import views

#url(regex and form action and website url, views.py name, nothing)
#url(nicole and laura, laura, laura)
urlpatterns = patterns('',
    url(r'^$', views.sell_form, name='sell_form'),
    url(r'^submit/$', views.sell_submit, name='sell_form'),
)
