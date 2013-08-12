from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^manager$', 'mng.views.base', name='manager'),
    url(r'^manager-fnc$', 'mng.views.fnc', name='mng-fnc'),
    url(r'^manager-wiki$', 'mng.views.wiki', name='mng-wiki'),
    url(r'^manager-sales$', 'mng.views.sales', name='mng-sales'),
    url(r'^manager-wrh$', 'mng.views.wrh', name='mng-wrh'),
    url(r'^manager-emp$', 'mng.views.emp', name='mng-emp'),


    )
