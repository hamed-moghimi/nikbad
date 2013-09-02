from django.contrib import admin
from wiki.models import Product
from wiki.models import Wiki
from wiki.models import Contract
from wiki.models import ReturnRequest
from wiki.models import ConRequest
from wiki.models import ConCancel

admin.site.register(Product)
admin.site.register(Wiki)
admin.site.register(Contract)
admin.site.register(ReturnRequest)
admin.site.register(ConRequest)
admin.site.register(ConCancel)



