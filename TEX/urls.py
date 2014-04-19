from django.conf.urls import patterns, include, url
from django.contrib import admin
from search import views
import django_cron
django_cron.autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^helloDjango/', include('helloDjango.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^book/', include('book.urls')),
    url(r'^sell/', include('sell.urls')),
    url(r'^buy/', include('buy.urls')),
    url(r'^account/', include('account.urls')),
    url(r'.*', "search.views.error_page"),
)
#test
