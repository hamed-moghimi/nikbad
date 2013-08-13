from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'fnc.views.index', name='fnc-index'),
	url(r'^financeReport$', 'fnc.views.gozaresh_mali', name='fnc-gozaresh-mali'),
	url(r'^registerEmployee$', 'fnc.views.sabtenam_karmand', name='fnc-sabtenam-karmand'),
	url(r'^employees$', 'fnc.views.karmandan', name='fnc-karmandan'),
	url(r'^EmpDetail/(?P<epId>\d+)$', 'fnc.views.karmand_detail', name='fnc-karmand-detail'),
	url(r'^add$', 'fnc.views.add_sanad', name='fnc-add-sanad'),
)
