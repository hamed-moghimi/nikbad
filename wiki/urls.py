from django.conf.urls import patterns, url

urlpatterns = patterns('',
     url(r'^$', 'wiki.views.index', name='wiki-index'),
     url(r'^goodslist$', 'wiki.views.goodsList', name='goods-list'),
     url(r'^register$', 'wiki.views.register', name='wiki-register'),
     url(r'^success$', 'wiki.views.success', name='wiki-success'),
     url(r'^addProduct$', 'wiki.views.addproduct', name='add-product'),
     url(r'^deleteProduct$', 'wiki.views.deleteproduct', name='delete-product'),
     url(r'^DateForm$', 'wiki.views.wrhorders', name='wrh-order'),
     url(r'^returnrequest$', 'wiki.views.returnrequest', name='return-req'),
     url(r'^salesreport$', 'wiki.views.salesreport', name='sales-report'),
     url(r'^wrhproducts$', 'wiki.views.wrhproducts', name='wrh-product'),
     url(r'^productEdit/(?P<gId>\d+)$', 'wiki.views.editProduct', name='product-edit'),
)
