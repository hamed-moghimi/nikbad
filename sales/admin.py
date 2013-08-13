from django.contrib.admin.options import ModelAdmin, TabularInline, StackedInline
from django.contrib import admin

from sales.models import *


admin.site.register(SaleBill)
admin.site.register(SaleBill_Product)

admin.site.register(MarketBasket)
admin.site.register(MarketBasket_Product)

class SpecInline(TabularInline):
    model = Specification
    extra = 5


class ImageInline(StackedInline):
    model = AdImage
    extra = 3

class AdModelAdmin(ModelAdmin):
    inlines = [SpecInline, ImageInline]

admin.site.register(Ad, AdModelAdmin)
admin.site.register(Specification)
admin.site.register(AdImage)