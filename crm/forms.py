from django.forms.models import ModelForm
from crm.models import Customer
from django.forms import *

class CustomerForm(ModelForm):
    #sword = forms.CharField(widget = forms.PasswordInput)
   # password = forms.CharField(label="Password", widget=forms.PasswordInput)
    class Meta:
        model = Customer
        fields = ['username',  "password" , 'first_name', 'last_name', 'gender' , 'phone'  , 'email'  , 'postal_code', 'city' , 'address' ]

