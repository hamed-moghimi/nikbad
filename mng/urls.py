from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^manager$', 'mng.views.index', name='manager'),
    url(r'^contract$', 'mng.views.newContract', name='contract'),

)
