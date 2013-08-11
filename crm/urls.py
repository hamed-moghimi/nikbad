from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^profile$', 'crm.views.index', name='crm-profile'),
    url(r'^edit$', 'crm.views.edit', name='crm-edit'),
    url(r'^status$', 'crm.views.status', name='crm-status'),
    url(r'^signUp-successful$', 'crm.views.success', name='crm-signUpsuccessful'),
    url(r'^edit-successful$', 'crm.views.edit_success', name='crm-editsuccessful'),
    url(r'^signUp$', 'crm.views.signUp', name='crm-signUp'),
    url(r'^feedback$', 'crm.views.feedback', name='crm-feedback'),

)
