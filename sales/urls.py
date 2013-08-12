from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'sales.views.index', name='sales-index'),
    url(r'^category/(?P<catID>\d+)$', 'sales.views.category', name='sales-category'),
    url(r'^vitrin/(?P<itemCode>\d+)$', 'sales.views.detailsPage', name='sales-vitrin'),
    url(r'basket$', 'sales.views.marketBasket', name='sales-basket'),
    #url(r'^newBuy$', 'sales.views.newBuy', name='sales-newBuy'),
)
