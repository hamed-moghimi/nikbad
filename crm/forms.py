#-*- coding:utf-8 -*-
from django.forms.models import ModelForm
from crm.models import Customer
from django.forms import *

class checkCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['username' , 'first_name', 'last_name', 'gender' , 'phone'  , 'email'  , 'postal_code', 'city' , 'address' ]


class CustomerForm(ModelForm):
    password = CharField(label= u"گذر واژه" ,widget=PasswordInput)
    repassword = CharField(label= u"تکرار گذرواژه" ,widget=PasswordInput)
    class Meta:
        model = Customer
        fields = ['username','password','repassword' , 'first_name', 'last_name', 'gender' , 'phone'  , 'email'  , 'postal_code', 'city' , 'address' ]


    def clean_repassword(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('repassword')
        # password and password2 must be the same
        print( password , password2)
        if password != password2:
            raise forms.ValidationError(u"گذرواژه و تکرار ان یکسان نیست")

        return self.cleaned_data.get('password')


class EditForm(ModelForm):
    class Meta:
        model = Customer
        fields = [ 'first_name', 'last_name' , 'phone'  , 'email','postal_code'  , 'address' ]


