from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^profile$', 'crm.views.index', name='crm-index'),
    url(r'^edit$', 'crm.views.edit', name='crm-index'),
    url(r'^status$', 'crm.views.status', name='crm-index'),
    url(r'^signUp-successful$', 'crm.views.success', name='crm-index'),
    url(r'^signUp$', 'crm.views.signUp', name='crm-index'),
)
