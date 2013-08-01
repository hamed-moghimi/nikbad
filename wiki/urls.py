from django.conf.urls import patterns, url

urlpatterns = patterns('',
     url(r'^goodslist$', 'wiki.views.goodsList', name='wiki-index'),
)
