from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'sales.views.index', name='sales-index'),
    url(r'^newBuy$', 'sales.views.newBuy', name='sales-newBuy'),
)
