from django.conf.urls import patterns, url

urlpatterns = patterns('sales.views',
                       url(r'^$', 'index', name = 'sales-index'),
                       url(r'^category/(?P<catID>\d+)$', 'category', name = 'sales-category'),
                       url(r'^vitrin/(?P<itemCode>\d+)$', 'detailsPage', name = 'sales-vitrin'),
                       url(r'^vitrin_edit/(?P<itemCode>\d+)$', 'adEdit', name = 'sales-adEdit'),
                       url(r'basket$', 'marketBasket', name = 'sales-basket'),
                       url(r'basket_ajax/(?P<pId>\d+)$', 'addToMarketBasket', name = 'sales-addBasket'),
                       url(r'^newBuy$', 'newBuy', name = 'sales-finishBuy'),
                       url(r'^search$', 'search', name = 'sales-search'),
                       url(r'^pdf/SaleBill/(?P<sbID>\d+)$', 'saleBillPDF', name = 'sales-SaleBillPDF'),
)
