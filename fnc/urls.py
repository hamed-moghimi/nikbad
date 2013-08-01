from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'fnc.views.index', name='fnc-index'),
	url(r'^$', 'fnc.views.index', name='fnc-index'),

)
