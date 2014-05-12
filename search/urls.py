from django.conf.urls import patterns, url
from search import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^isbn/$', views.isbn, name='search'),
    url(r'^title/$', views.title, name='search'),
    url(r'^author/$', views.author, name='search'),
    url(r'^course/$', views.course, name='search')
)