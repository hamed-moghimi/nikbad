from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^manager$', 'mng.views.index', name = 'manager'),
                       url(r'^manager-fnc$', 'mng.views.gozaresh_mali', name = 'mng-fnc'),
                       url(r'^manager-wiki-select$', 'mng.views.wiki_select', name = 'mng-wiki-select'),
                       url(r'^manager-wiki/(?P<wId>\d+)$', 'mng.views.wiki', name = 'mng-wiki'),
                       url(r'^manager-wrh$', 'mng.views.wrh', name = 'mng-wrh'),
                       url(r'^manager-emp$', 'mng.views.karmandan', name = 'mng-emp'),
                       url(r'^manager-emp-detail/(?P<epId>\d+)$', 'mng.views.karmand_detail', name = 'mng-emp-detail'),
                       url(r'^manager-newemp$', 'mng.views.sabtenam_karmand', name = 'mng-newemp'),
                       url(r'^manager-sales$', 'mng.views.sales', name = 'mng-sales'),
                       url(r'^manager-sales-detail/(?P<wId>\d+)$', 'mng.views.saleDetail', name = 'mng-sale-detail'),
                       url(r'^manager-returned$', 'mng.views.returned', name = 'mng-return'),
                       url(r'^manager-cont/(?P<wId>\d+)$', 'mng.views.newContract', name = 'mng-cont'),
                       url(r'^manager-user$', 'mng.views.newUser', name = 'mng-newuser'),
                       url(r'^contractDetail/(?P<wId>\d+)$', 'mng.views.contractDetail', name = 'contract-detail'),
                       url(r'^contractEdit/(?P<wId>\d+)$', 'mng.views.contractEdit', name = 'contract-edit'),
                       url(r'^contractRequest$', 'mng.views.conReq', name = 'contract-request'),
                       url(r'^employees$', 'mng.views.karmandan', name = 'fnc-karmandan'),
                       url(r'^EmpDetail/(?P<epId>\d+)$', 'mng.views.karmand_detail', name = 'fnc-karmand-detail'),
                       url(r'^EmpDetail2/(?P<epId>\d+)$', 'mng.views.karmand_detail_2', name = 'fnc-karmand-detail-2'),
                       url(r'^daftarKol$', 'mng.views.daftar_kol', name = 'fnc-daftar-kol'),
                       url(r'^daftarKol2/(?P<daftarId>\d+)$', 'mng.views.daftar_kol_2', name = 'fnc-daftar-kol-2'),
                       url(r'^tarazAzmayeshi$', 'mng.views.taraz_azmayeshi', name = 'fnc-taraz-azmayeshi'),
                       url(r'^tarazAzmayeshi2/(?P<tarazId>\d+)$', 'mng.views.taraz_azmayeshi_2',
                           name = 'fnc-taraz-azmayeshi-2'),
                       url(r'^addHesab$', 'mng.views.add_hesab', name = 'fnc-add-hesab'),
                       url(r'^residEmp$', 'mng.views.resid_emp', name = 'fnc-resid-emp'),
                       url(r'^conCancel$', 'wiki.views.cancelContract', name = 'con-can'),


)
