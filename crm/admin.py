from django.contrib.admin.options import ModelAdmin
from crm.models import *
from django.contrib import admin

admin.site.register(Customer)


class FeedbackAdmin(ModelAdmin):
    fields = ['content', 'product']
    readonly_fields = ['content', 'product']


admin.site.register(Feedback, FeedbackAdmin)
