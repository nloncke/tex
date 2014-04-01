from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TEX.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'search.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^helloDjango/', include('helloDjango.urls')),
    url(r'^search/', include('search.urls')),
)
#test