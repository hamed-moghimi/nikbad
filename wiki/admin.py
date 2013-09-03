from django.contrib import admin
from wiki.models import Product
from wiki.models import Wiki
from wiki.models import Contract
from wiki.models import ReturnRequest, Brand
from wiki.models import ConRequest
from wiki.models import ConCancel, SubCat, Category

admin.site.register(Product)
admin.site.register(Wiki)
admin.site.register(Contract)
admin.site.register(ReturnRequest)
admin.site.register(ConRequest)
admin.site.register(ConCancel)
admin.site.register(Brand)


class SubCatAdmin(admin.ModelAdmin):
    list_filter = ['category']
    list_display = ['name', 'category']
    # exclude = ['image']
    # readonly_fields = ['ad', 'title', 'thumbnail', 'checked']

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']

admin.site.register(SubCat, SubCatAdmin)
admin.site.register(Category, CategoryAdmin)