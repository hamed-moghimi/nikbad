# -*- encoding: utf-8 -*-
from django.forms.models import ModelForm
from contrib.forms import jDateField
from fnc.models import *
from models import Employee
from django.forms import *


class EmployeeForm(ModelForm):
	class Meta:
		model = Employee
		fields = ['name', 'family_name', 'national_id', 'mobile_num', 'tel_num', 'address',
				  'salary']
        name=CharField=()

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
        fields = ['account_bedeh','account_bestan','amount', 'description']
    def clean(self):
        cleaned_data = super(AddForm, self).clean()
        bestan = cleaned_data.get("account_bestan")
        bedeh = cleaned_data.get("account_bedeh")
        if bestan==bedeh:
            raise ValidationError(u"حساب بستانکار و بدهکار نمیتوانند یکسان باشند")
        else:
            return cleaned_data

class AddHesab(ModelForm):
	class Meta:
		model = Account
		fields = ['name','amount']