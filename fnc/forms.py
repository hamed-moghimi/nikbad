# -*- encoding: utf-8 -*-
from django.forms.models import ModelForm
from fnc.models import CostBenefit
from models import Employee
from django.forms import *


class EmployeeForm(ModelForm):
	class Meta:
		model = Employee
		fields = ['name', 'family_name', 'national_id', 'mobile_num', 'tel_num', 'address', 'gender', 'marriage_status',
				  'salary']


class DateForm(Form):
	startDate = DateField(label=u'از تاریخ ')
	endDate = DateField(label=u' تا تاریخ')

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
		model=CostBenefit
		fields=['bedeh', 'bestan', 'description']