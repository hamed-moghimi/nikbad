# -*- coding: utf-8 -*-
from django.contrib.admin.filters import SimpleListFilter

from django.contrib.admin.options import ModelAdmin, TabularInline, StackedInline
from django.contrib import admin
from django.contrib.auth.models import User
from django.forms.fields import ImageField
from django.forms.models import ModelForm

from sales.models import *


class SBAdmin(ModelAdmin):
    list_display = ['id']


admin.site.register(SaleBill, SBAdmin)
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
    list_display = ['__unicode__', 'popularity']
    inlines = [SpecInline, ImageInline]


admin.site.register(Ad, AdModelAdmin)
admin.site.register(Specification)


class AdImageAdmin(ModelAdmin):
    list_filter = ['checked']
    list_display = ['title', 'thumbnail']
    exclude = ['image']
    readonly_fields = ['ad', 'title', 'thumbnail']

    def approve(self, request, queryset):
        queryset.update(checked = True)

    approve.short_description = u'تایید تصاویر'

    actions = [approve]


# This line is very important! :D
admin.site.get_action('delete_selected').short_description = u'حذف %(verbose_name_plural)s'
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