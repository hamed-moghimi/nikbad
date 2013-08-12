from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^manager$', 'mng.views.index', name='manager'),
    url(r'^manager-fnc$', 'fnc.views.gozaresh_mali', name='mng-fnc'),
    url(r'^manager-wiki-select$', 'mng.views.wiki_select', name='mng-wiki-select'),
    url(r'^manager-wiki/(?P<wId>\d+)$', 'mng.views.wiki', name='mng-wiki'),
    url(r'^manager-wrh$', 'mng.views.index', name='mng-wrh'),
    url(r'^manager-emp$', 'fnc.views.karmandan', name='mng-emp'),
    url(r'^manager-emp-detail/(?P<epId>\d+)$', 'fnc.views.karmand_detail', name='mng-emp-detail'),
    url(r'^manager-newemp$', 'fnc.views.sabtenam_karmand', name='mng-newemp'),
    url(r'^manager-sales$', 'mng.views.sales', name='mng-sales'),
    url(r'^manager-cont$', 'mng.views.newContract', name='mng-cont'),


)
