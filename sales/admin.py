from django.contrib.admin.options import ModelAdmin, TabularInline, StackedInline
from django.contrib import admin
from django.contrib.auth.models import User
from django.forms.fields import ImageField
from django.forms.models import ModelForm

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


class AdImageAdmin(ModelAdmin):
    list_display = ['title', 'thumbnail']


admin.site.register(AdImage, AdImageAdmin)

# class UserAdmin (admin.ModelAdmin):
#
#     def queryset (self, request):
#         qs = User.objects.filter(is_staff = False)
#         ordering = self.get_ordering(request)
#         if ordering:
#             qs = qs.order_by(*ordering)
#         return qs
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)