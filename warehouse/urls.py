from django.conf.urls import patterns, url
from warehouse.views import reports

urlpatterns = patterns('',
                       url(r'^$', 'warehouse.views.index', name='warehouse-index'),

                       # url haaye marbut be havaleehaye jadid ham va3 anbaardar ham va3 deliveryman
                       url(r'^(?P<org>\S+)NewOrder$', 'warehouse.views.new_order', name='warehouse-index-test'),
                       url(r'^(?P<org>\S+)OrdersPanel$', 'warehouse.views.order_panel', name='warehouse-index-test'),
                       url(r'^(?P<org>\S+)ReadyOrder$', 'warehouse.views.ready_order', name='warehouse-index-test'),
                       url(r'^(?P<org>\S+)OrdersReadyPanel$', 'warehouse.views.ready_order_panel', name='warehouse-index-test'),
                       url(r'^(?P<org>\S+)ConfirmOrder/(?P<pid>\d+)$', 'warehouse.views.confirm_order',
                           name='warehouse-index-test'),
                       url(r'^(?P<org>\S+)ConfirmReadyOrder/(?P<pid>\d+)$', 'warehouse.views.confirm_ready_order',
                           name='warehouse-index-test'),

                       #url haaye marbut be sabte vorude kalaa be anbaar
                       url(r'^(?P<org>\S+)WRHDelivery$', 'warehouse.views.delivery_wiki_select', name='warehouse-index-test'),
                       url(r'^WRHDelivery-Panel$', 'warehouse.views.delivery_wiki_select2', name='warehouse-index-test'),
                       url(r'^(?P<org>\S+)WRHDelivery-Panel$', 'warehouse.views.delivery_wiki_select2', name='warehouse-index-test'),
                       url(r'^(?P<org>\S+)WRHDeliveryConfirmation$', 'warehouse.views.confirm_wrh_delivery',
                           name='warehouse-index-test'),
                       url(r'^(?P<org>\S+)WRHDelivery-next/(?P<pid>\d+)$', 'warehouse.views.delivery_product_select',
                           name='warehouse-index-tiny_order'),
                       url(r'^WRHDeliveryConfirmation$', 'warehouse.views.confirm_wrh_delivery',
                           name='warehouse-index-test'),
                       url(r'^WRHDelivery-next/(?P<pid>\d+)$', 'warehouse.views.delivery_product_select',
                           name='warehouse-index-tiny_order'),

                       #url haaye marbut be bargashte kaalaaye mayoub az moshtari
                       url(r'^(?P<org>\S+)CustomerReturn$', 'warehouse.views.customer_return', name='warehouse-index-test'),
                       url(r'^(?P<org>\S+)CustomerReturn-Panel$', 'warehouse.views.customer_return_panel', name='warehouse-index-test'),
                       url(r'^(?P<org>\S+)CustomerReturn-next$', 'warehouse.views.customer_return_next',
                           name='warehouse-index-tiny_order'),
                       url(r'^(?P<org>\S+)CustomerReturn-next/(?P<pid>\d+)/(?P<kid>\d+)$', 'warehouse.views.customer_return_next2',
                           name='warehouse-index-tiny_order'),
                       url(r'^(?P<org>\S+)ConfirmReturn/(?P<pid>\d+)/(?P<kid>\d+)/(?P<cid>\d+)$', 'warehouse.views.confirm_return',
                           name='warehouse-index-tiny_order'),
                       url(r'^ConfirmReturn/(?P<pid>\d+)/(?P<kid>\d+)/(?P<cid>\d+)$', 'warehouse.views.confirm_return',
                           name='warehouse-index-tiny_order'),

                       #url haaye marbut be reside kalaahaaye havale be moshtari ya wiki
                       url(r'^(?P<org>\S+)Cust-wiki-ReceiptDelivery$', 'warehouse.views.ReceiptDelivery', name='warehouse-index-test'),
                       url(r'^(?P<org>\S+)Cust-wiki-ReceiptDelivery-Panel$', 'warehouse.views.ReceiptDelivery_Panel', name='warehouse-index-test'),
                       url(r'^(?P<org>\S+)ReceiptDetail$', 'warehouse.views.receipt_detail',
                           name='warehouse-index-tiny_order'),
                       # url(r'^(?P<org>\S+)ReceiptDetail/(?P<pid>\d+)$', 'warehouse.views.receipt_detail',
                       #     name='warehouse-index-tiny_order'),
                       url(r'^(?P<org>\S+)ConfirmReceipt/(?P<pid>\d+)$', 'warehouse.views.confirm_receipt',
                           name='warehouse-index-tiny_order'),

                       #url marbut be report haa
                       url(r'^(?P<org>\S+)Report/(?P<menu_id>\d+)$', 'warehouse.views.reports',
                           name='warehouse-index-tiny_order'),
                       url(r'^(?P<org>\S+)ReportReceipt_Panel/(?P<menu_id>\d+)$', 'warehouse.views.report_receipt_panel',
                           name='warehouse-index-tiny_order'),
                       url(r'^(?P<org>\S+)ReportReceipt_Panel/(?P<menu_id>\d+)?page=(?P<num>\d+)$', 'warehouse.views.report_receipt_panel',
                           name='warehouse-index-tiny_order'),
                       url(r'^(?P<org>\S+)ReportProduct_Panel/(?P<menu_id>\d+)$', 'warehouse.views.report_product_panel',
                           name='warehouse-index-tiny_order'),
                       url(r'^(?P<org>\S+)ReportProduct_Panel/(?P<menu_id>\d+)?page=(?P<num>\d+)$', 'warehouse.views.report_product_panel',
                           name='warehouse-index-tiny_order'),
                       url(r'^(?P<org>\S+)ReportReceiptDelivery$', 'warehouse.views.report_receipt_delivery',
                           name='warehouse-index-test'),
                       url(r'^(?P<org>\S+)ReportReceiptDelivery_Panel$', 'warehouse.views.report_receipt_delivery2',
                           name='warehouse-index-test'),
                       url(r'^(?P<org>\S+)ReportReceiptDelivery_Panel?page=(?P<num>\d+)$$', 'warehouse.views.report_receipt_delivery2',
                           name='warehouse-index-test'),
                       url(r'^(?P<org>\S+)ReportDetail/(?P<pid>\d+)/(?P<kid>\d+)$', 'warehouse.views.report_detail',
                           name='warehouse-index-tiny_order'),


                       #url haaye marbut be taghire noghteye sefaresh
                       url(r'^(?P<org>\S+)OrderPoint$', 'warehouse.views.point_order', name='warehouse-index-test'),
                       url(r'^(?P<org>\S+)OrderPoint-Panel$', 'warehouse.views.point_orders_panel', name='warehouse-index-test'),
                       url(r'^(?P<org>\S+)OrderPoint-next$', 'warehouse.views.point_order_next',
                           name='warehouse-index-tiny_order'),
                       url(r'^(?P<org>\S+)OrderPoint-next/(?P<kid>\d+)$', 'warehouse.views.point_order_next2',
                           name='warehouse-index-tiny_order'),
                       url(r'^ConfirmOrderPoint/(?P<kid>\d+)/(?P<cid>\d+)$', 'warehouse.views.confirm_order_point',
                           name='warehouse-index-tiny_order'),
                       url(r'^(?P<org>\S+)ConfirmOrderPoint/(?P<kid>\d+)/(?P<cid>\d+)$', 'warehouse.views.confirm_order_point',
                           name='warehouse-index-tiny_order'),

)
