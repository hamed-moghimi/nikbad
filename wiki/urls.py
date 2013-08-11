from django.conf.urls import patterns, url

urlpatterns = patterns('',
     url(r'^goodslist$', 'wiki.views.goodsList', name='wiki-index'),
     url(r'^register$', 'wiki.views.register', name='wiki-index'),
     url(r'^success$', 'wiki.views.success', name='wiki-index'),
     url(r'^addProduct$', 'wiki.views.addproduct', name='wiki-index'),
     url(r'^deleteProduct$', 'wiki.views.deleteproduct', name='deleteproduct'),
     url(r'^DateForm$', 'wiki.views.wrhorders', name='wrh-order'),
     url(r'^returnrequest$', 'wiki.views.returnrequest', name='return-req'),
     # url(r'^wrhproducts$', 'wiki.views.wrhproducts', name='wrh-products'),
)
