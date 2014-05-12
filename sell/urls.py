from django.conf.urls import patterns, url
from sell import views

urlpatterns = patterns('',
    url(r'^$', views.sell_form, name='sell_form'),
    url(r'^submit/$', views.sell_submit, name='sell_form'),
    url(r'^edit/$', views.sell_edit, name='sell_form'),
    url(r'^edit/submit/$', views.sell_edit_submit, name='sell_form'),
)
