from django.forms.models import ModelForm
from models import Employee
from django.forms import *


class EmployeeForm(ModelForm):
	class Meta:
		model = Employee
		fields = ['name', 'family_name', 'national_id', 'mobile_num', 'tel_num', 'address', 'gender', 'marriage_status','salary']