from django.contrib.admin.options import ModelAdmin
from fnc.models import *
from django.contrib import admin

admin.site.register(CostBenefit)
admin.site.register(Employee)
admin.site.register(RollCall)
admin.site.register(SalaryFactor)
admin.site.register(GeneralAccount)
admin.site.register(Taraz)
admin.site.register(WikiFactor)
admin.site.register(Row)


class AccountAdmin(ModelAdmin):
    list_display = ['__unicode__', 'amount_display']
    fields = ['name']
    readonly_fields = ['name', 'amount_display']


admin.site.register(Account, AccountAdmin)
