from django.conf.urls import patterns, url
from book import views

#url(regex and form action and website url, views.py name, nothing)
#url(nicole and laura, laura, laura)
urlpatterns = patterns('',
    url(r'^$', views.book_index, name='book_index'),
    url(r'^follow/$', views.book_follow, name='book_follow'),
    url(r'^unfollow/$', views.book_unfollow, name='book_unfollow'),
)

