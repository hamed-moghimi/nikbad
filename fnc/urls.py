from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'fnc.views.index', name='fnc-index'),
	url(r'^test1$', 'fnc.views.gozaresh_mali', name='fnc-gozaresh-mali'),
	url(r'^test2$', 'fnc.views.sabtenam_karmand', name='fnc-sabtenam-karmand'),

)
