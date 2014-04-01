from django.conf.urls import patterns, url

from search import views

#url(regex and form action and website url, views.py name, nothing)
#url(nicole and laura, laura, laura)
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^isbn$', views.results, name='search/isbn')
)