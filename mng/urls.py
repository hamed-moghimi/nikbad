from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^manager$', 'mng.views.base', name='manager'),
    url(r'^manager-fnc$', 'fnc.views.gozaresh_mali', name='mng-fnc'),
    url(r'^manager-wiki-select$', 'mng.views.select_wiki', name='mng-select-wiki'),
    url(r'^manager-wiki/(?P<wId>\d+)$', 'mng.views.wiki', name='mng-wiki'),
    url(r'^manager-sales$', 'mng.views.sales', name='mng-sales'),
    url(r'^manager-wrh$', 'mng.views.wrh', name='mng-wrh'),
    url(r'^manager-newemp$', 'fnc.views.sabtenam_karmand', name='mng-newemp'),
    url(r'^manager-emp$', 'fnc.views.karmandan', name='mng-emp'),
    url(r'^manager-emp/(?P<epId>\d+)$', 'fnc.views.karmand_detail', name='mng-emp-detail'),

    )
