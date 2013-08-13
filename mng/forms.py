#-*- coding:utf-8 -*-
from django.contrib.auth.models import User
from wiki.models import Contract
from django.forms.models import ModelForm
from django.forms import *

class ContractForm(ModelForm):
    class Meta:
        model = Contract

class userForm(ModelForm):
    password = CharField(label= u"گذر واژه" ,widget=PasswordInput)
    repassword = CharField(label= u"تکرار گذرواژه" ,widget=PasswordInput)
    is_delivery = BooleanField(label= u"حمل و نقل" , required=False )
    is_fnc = BooleanField(label= u"انباردار"  , required=False)
    is_wrh = BooleanField(label= u"امور مالی"  , required=False)
    class Meta:
        model = User
        fields = ['username','password','repassword' , 'first_name', 'last_name'  , 'email', 'is_delivery' ,'is_fnc' ,'is_wrh' ]

    def clean_repassword(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('repassword')
        # password and password2 must be the same
        print( password , password2)
        if password != password2:
            raise forms.ValidationError(u"گذرواژه و تکرار ان یکسان نیست")

        return self.cleaned_data.get('password')
