from django.conf.urls import patterns, url
from book import views

urlpatterns = patterns('',
    url(r'^$', views.book_index, name='book_index'),
    url(r'^add/$', views.add, name='book_add'),
)

