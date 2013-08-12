from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # index url
    url(r'^$', 'sales.views.index', name='index'),
    url(r'^login$', 'contrib.views.login', name='login'),
    url(r'^logout', 'contrib.views.logout', name='logout'),

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
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # for serving media files