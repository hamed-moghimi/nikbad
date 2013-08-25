#-*- coding:utf-8 -*-
from django.contrib.auth.models import User
from contrib.forms import jDateField
from wiki.models import Contract
from django.forms.models import ModelForm
from django.forms import *

class ContractForm(ModelForm):
    startDate = jDateField(label=u"تاریخ شروع قرارداد")
    expDate = jDateField(label=u"تاریخ پایان قرارداد")
    wiki= CharField(label=u"نام ویکی")
    fee = IntegerField(label=u"هزینه آبونمان (تومان)")
    precent = IntegerField(label=u"کارمزد سراب (تومان)")
    class Meta:
        model = Contract

class userForm(ModelForm):
    password = CharField(label= u"گذر واژه" ,widget=PasswordInput)
    repassword = CharField(label= u"تکرار گذرواژه" ,widget=PasswordInput)
    is_delivery = BooleanField(label= u"حمل و نقل" , required=False )
    is_wrh = BooleanField(label= u"انباردار"  , required=False)
    is_fnc = BooleanField(label= u"امور مالی"  , required=False)
    ssn = RegexField(label=u"شماره ملی" ,regex="\d{10}",max_length=10 , error_messages={'invalid' : u"شماره ملی باید 10 رقمی باشد"})


    class Meta:
        model = User
        fields = ['username','password','repassword' ,'ssn', 'first_name', 'last_name'  , 'email','is_delivery' ,'is_fnc' ,'is_wrh' ]


    def clean_is_wrh(self):
        print "hamedooooo"
        deliv = self.cleaned_data.get('is_delivery')
        fnc = self.cleaned_data.get('is_fnc')
        wrh = self.cleaned_data.get('is_wrh')

        if deliv==False and fnc ==False and wrh==False:
            raise forms.ValidationError(u"حداقل یکی از نقش ها برای کاربر باید انتخاب شود")
        return self
    def clean_repassword(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('repassword')
        # password and password2 must be the same
        print( password , password2)

        if password != password2:
            raise forms.ValidationError(u"گذرواژه و تکرار ان یکسان نیست")

        return self.cleaned_data.get('password')
