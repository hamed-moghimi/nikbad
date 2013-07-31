from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # index url
    url(r'^$', 'sales.views.index2', name='index'),

    # subsystem urls
    url(r'^sales/', include('sales.urls')),
    url(r'^wiki/', include('wiki.urls')),
    url(r'^crm/', include('crm.urls')),
    url(r'^warehouse/', include('warehouse.urls')),
    url(r'^fnc/', include('fnc.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
