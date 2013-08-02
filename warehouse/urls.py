from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'warehouse.views.index', name='warehouse-index'),
    url(r'^NewOrder$', 'warehouse.views.test', name='warehouse-index-test'),
    url(r'^Tiny_Order/(?P<pid>\d+)$', 'warehouse.views.tiny_order', name='warehouse-index-tiny_order'),
    url(r'^NewOrdersBack$', 'warehouse.views.testback', name='warehouse-index-test'),
    url(r'^WRHDelivery2$', 'warehouse.views.delivery_wiki_select2', name='warehouse-index-test'),
    url(r'^WRHDelivery$', 'warehouse.views.delivery_wiki_select', name='warehouse-index-test'),
    url(r'^ConfirmationWRHDelivery$', 'warehouse.views.confirm_wrh_delivery', name='warehouse-index-test'),
    url(r'^WRHDelivery-next/(?P<pid>\d+)$', 'warehouse.views.delivery_product_select', name='warehouse-index-tiny_order'),
)
