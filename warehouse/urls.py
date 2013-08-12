from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'warehouse.views.index', name='warehouse-index'),

    # url haaye marbut be havaleehaye jadid e anbaardaar
    url(r'^NewOrder$', 'warehouse.views.new_order', name='warehouse-index-test'),
    url(r'^NewOrdersBack$', 'warehouse.views.new_order_back', name='warehouse-index-test'),
    url(r'^ConfirmOrder/(?P<pid>\d+)$', 'warehouse.views.confirm_order', name='warehouse-index-test'),
    url(r'^Tiny_Order/(?P<pid>\d+)$', 'warehouse.views.tiny_order', name='warehouse-index-tiny_order'),

    #url haaye marbut be havaalehayae amaadeye xoruj va3 delivery man
    url(r'^ReadyOrder$', 'warehouse.views.ready_order', name='warehouse-index-test'),
    url(r'^ReadyTiny_Order/(?P<pid>\d+)$', 'warehouse.views.ready_tiny_order', name='warehouse-index-tiny_order'),
    url(r'^ReadyOrder2$', 'warehouse.views.ready_order_back', name='warehouse-index-test'),
    url(r'^ConfirmReadyOrder/(?P<pid>\d+)$', 'warehouse.views.confirm_ready_order', name='warehouse-index-test'),

    #url haaye marbut be sabte vorude kalaa be anbaar
    url(r'^WRHDelivery$', 'warehouse.views.delivery_wiki_select', name='warehouse-index-test'),
    url(r'^WRHDelivery2$', 'warehouse.views.delivery_wiki_select2', name='warehouse-index-test'),
    url(r'^ConfirmationWRHDelivery$', 'warehouse.views.confirm_wrh_delivery', name='warehouse-index-test'),
    url(r'^WRHDelivery-next/(?P<pid>\d+)$', 'warehouse.views.delivery_product_select', name='warehouse-index-tiny_order'),

    #url haaye marbut be bargashte kaalaaye mayoub az moshtari
    url(r'^CustomerReturn$', 'warehouse.views.customer_return', name='warehouse-index-test'),
    url(r'^CustomerReturn2$', 'warehouse.views.customer_return2', name='warehouse-index-test'),
    url(r'^CustomerReturn-next/(?P<pid>\d+)/(?P<kid>\d+)$', 'warehouse.views.customer_return_next', name='warehouse-index-tiny_order'),
    url(r'^ConfirmReturn/(?P<pid>\d+)/(?P<kid>\d+)/(?P<cid>\d+)$', 'warehouse.views.confirm_return', name='warehouse-index-tiny_order'),

    #url haaye marbut be reside kalaahaaye havale be moshtari ya wiki
    url(r'^ReceiptDelivery$', 'warehouse.views.ReceiptDelivery', name='warehouse-index-test'),
    url(r'^ReceiptDelivery2$', 'warehouse.views.ReceiptDelivery2', name='warehouse-index-test'),
    url(r'^ReceiptDetail/(?P<pid>\d+)$', 'warehouse.views.receipt_detail', name='warehouse-index-tiny_order'),
    url(r'^ConfirmReceipt/(?P<pid>\d+)$', 'warehouse.views.confirm_receipt', name='warehouse-index-tiny_order'),
)
