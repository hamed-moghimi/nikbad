from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'sales.views.index', name='sales-index'),
)
