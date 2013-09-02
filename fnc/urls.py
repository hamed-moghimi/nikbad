from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'fnc.views.index', name='fnc-index'),
	url(r'^financeReport$', 'fnc.views.gozaresh_mali', name='fnc-gozaresh-mali'),
	url(r'^registerEmployee$', 'fnc.views.sabtenam_karmand', name='fnc-sabtenam-karmand'),
	url(r'^employees$', 'fnc.views.karmandan', name='fnc-karmandan'),
	url(r'^EmpDetail/(?P<epId>\d+)$', 'fnc.views.karmand_detail', name='fnc-karmand-detail'),
	url(r'^EmpDetail2/(?P<epId>\d+)$', 'fnc.views.karmand_detail_2', name='fnc-karmand-detail-2'),
	url(r'^add$', 'fnc.views.add_sanad', name='fnc-add-sanad'),
    url(r'^daftarKol$', 'fnc.views.daftar_kol', name='fnc-daftar-kol'),
    url(r'^daftarKol2/(?P<daftarId>\d+)$', 'fnc.views.daftar_kol_2', name='fnc-daftar-kol-2'),
    url(r'^tarazAzmayeshi$', 'fnc.views.taraz_azmayeshi', name='fnc-taraz-azmayeshi'),
    url(r'^tarazAzmayeshi2/(?P<tarazId>\d+)$', 'fnc.views.taraz_azmayeshi_2', name='fnc-taraz-azmayeshi-2'),
    url(r'^addHesab$', 'fnc.views.add_hesab', name='fnc-add-hesab'),
)
