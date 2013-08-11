from django.forms.models import ModelForm
from crm.models import Customer
from django.forms import *

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['username','password' , 'first_name', 'last_name', 'gender' , 'phone'  , 'email'  , 'postal_code', 'city' , 'address' ]

class EditForm(ModelForm):
    class Meta:
        model = Customer
        fields = [ 'first_name', 'last_name' , 'phone'  , 'email'  , 'address' ]


