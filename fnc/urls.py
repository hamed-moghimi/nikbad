from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'fnc.views.index', name='fnc-index'),
	url(r'test^$', 'fnc.views.gozaresh_mali', name='fnc-gozaresh-mali'),

)
