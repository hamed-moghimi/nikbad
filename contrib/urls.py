from django.conf.urls import patterns, url

urlpatterns = patterns('',
        url(r'^$', 'contrib.views.bank', name='contrib-bank'),
)