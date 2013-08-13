from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'sales.views.index', name = 'sales-index'),
                       url(r'^category/(?P<catID>\d+)$', 'sales.views.category', name = 'sales-category'),
                       url(r'^vitrin/(?P<itemCode>\d+)$', 'sales.views.detailsPage', name = 'sales-vitrin'),
                       url(r'^vitrin_edit/(?P<itemCode>\d+)$', 'sales.views.adEdit', name = 'sales-adEdit'),
                       url(r'basket$', 'sales.views.marketBasket', name = 'sales-basket'),
                       url(r'basket_ajax/(?P<pId>\d+)$', 'sales.views.addToMarketBasket', name = 'sales-addBasket'),
                       #url(r'^newBuy$', 'sales.views.newBuy', name='sales-newBuy'),
)
