# -*- encoding: utf-8 -*-
from django.forms.models import ModelForm
from contrib.forms import jDateField
from fnc.models import *
from models import Employee
from django.forms import *


class EmployeeForm(ModelForm):
    name = CharField(required=True, label=u"نام")
    email = EmailField(label=u"رایانامه", required=True, help_text="a@b.com")
    tel_num = RegexField(label=u"شماره تماس ثابت", help_text="021-88888888", regex="\d{7,}",
                       error_messages={'invalid': u"تلفن ثابت 11 رقمی است"})
    address = CharField(widget=Textarea(), label=u"نشانی محل سکونت")
    mobile_num=RegexField(label=u"شماره همراه",
                          required=True,help_text="0912-3333333",
                          regex="\d{12}",error_messages={'invalid': u"شماره همراه 11 رقمی است"})
    class Meta:
        model = Employee
        fields = ['name', 'family_name', 'national_id', 'mobile_num', 'tel_num', 'email', 'address',
                  'salary']

    name = CharField = ()


class DateForm(Form):
    startDate = jDateField(label=u'از تاریخ ')
    endDate = jDateField(label=u' تا تاریخ')

    def clean(self):
        cleaned_data = super(DateForm, self).clean()
        startDate = cleaned_data.get("startDate")
        endDate = cleaned_data.get("endDate")
        if endDate and startDate:
        # Only do something if both fields are valid so far.
            if startDate > endDate:
                raise ValidationError(u'تاریخ وارد شده نامعتبر است.')
            # Always return the full collection of cleaned data.
        return cleaned_data


class AddForm(ModelForm):
    class Meta:
        model = CostBenefit
        fields = ['account_bedeh', 'account_bestan', 'amount', 'description']

    def clean(self):
        cleaned_data = super(AddForm, self).clean()
        bestan = cleaned_data.get("account_bestan")
        bedeh = cleaned_data.get("account_bedeh")
        if bestan == bedeh:
            raise ValidationError(u"حساب بستانکار و بدهکار نمیتوانند یکسان باشند")
        else:
            return cleaned_data


class AddHesab(ModelForm):
    class Meta:
        model = Account
        fields = ['name','amount']
    def clean(self):
        cleaned_data = super(AddHesab, self).clean()
        n = cleaned_data.get("name")
        count=Account.objects.filter(name=n).count()
        if count>0:
            print "ssssssssssssssssssss"
            raise ValidationError(u"این حساب موجود است")
        else:
            return cleaned_data
