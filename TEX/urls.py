from django.conf.urls import patterns, include, url
from django.contrib import admin
import django_cas
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TEX.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'account.views.validate'),
    url(r'^login/$', django_cas.views.login, name='login'),
    url(r'^logout/$', django_cas.views.logout, name='logout'),
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
