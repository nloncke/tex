from django.conf.urls import patterns, url
from buy import views

#url(regex and form action and website url, views.py name, nothing)
#url(nicole and laura, laura, laura)
urlpatterns = patterns('',
    url(r'^confirm/$', views.buy_confirmation, name='buy_confirmation'),
    #url(r'^follow/$', views.book_follow, name='book_follow'),
)
