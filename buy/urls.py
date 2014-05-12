from django.conf.urls import patterns, url
from buy import views

urlpatterns = patterns('',
    url(r'^confirm/$', views.buy_confirmation, name='buy_confirmation'),
    url(r'^bid/$', views.bid, name='bid'),
)
