from django.forms.models import ModelForm
from models import Employee
from django.forms import *
class EmployeeForm(ModelForm):

    class Meta:
        model = Employee