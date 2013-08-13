from django.conf.urls import patterns, url

urlpatterns = patterns('',
        url(r'^bank$', 'contrib.views.bank', name='contrib-bank'),
)