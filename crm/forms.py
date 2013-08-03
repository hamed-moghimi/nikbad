from django.forms.models import ModelForm
from crm.models import Customer

class CustomerForm(ModelForm):

    class Meta:
        model = Customer
        fields = ['username',  'password' , 'first_name', 'last_name', 'gender' , 'email'  , 'postal_code' , 'address' ]

