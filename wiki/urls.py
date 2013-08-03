from django.conf.urls import patterns, url

urlpatterns = patterns('',
     url(r'^goodslist$', 'wiki.views.goodsList', name='wiki-index'),
     url(r'^register$', 'wiki.views.register', name='wiki-index'),
     url(r'^success$', 'wiki.views.success', name='wiki-index'),
     url(r'^addProduct$', 'wiki.views.addProduct', name='wiki-index'),
     url(r'^deleteProduct$', 'wiki.views.deleteProduct', name='wiki-index'),
)
