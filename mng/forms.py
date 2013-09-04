#-*- coding:utf-8 -*-
from django.contrib.auth.models import User
from contrib.forms import jDateField
from wiki.models import Contract
from django.forms.models import ModelForm
from django.forms import *


class ContractForm(ModelForm):
    startDate = jDateField(label = u"تاریخ شروع قرارداد")
    expDate = jDateField(label = u"تاریخ پایان قرارداد")
    companyName = CharField(label = u"نام ویکی")
    fee = IntegerField(label = u"هزینه آبونمان (ریال)")
    percent = IntegerField(label = u"کارمزد سراب(درصد)")

    class Meta:
        model = Contract
        fields = ['companyName', 'startDate', 'expDate', 'max_goods', 'fee', 'percent']


class ContractEdit(ModelForm):
    startDate = jDateField(label = u"تاریخ شروع قرارداد")
    expDate = jDateField(label = u"تاریخ پایان قرارداد")
    # companyName= CharField(label=u"نام ویکی")
    fee = IntegerField(label = u"هزینه آبونمان (ریال)")
    percent = IntegerField(label = u"کارمزد سراب(ریال)")

    class Meta:
        model = Contract
        fields = ['startDate', 'expDate', 'max_goods', 'fee', 'percent']

        # def __init__(self, *args, **kwargs):
        #     super(ContractForm, self).__init__(*args, **kwargs)
        #     if 'instance' in kwargs:
        #         self.fields['wiki'].value = unicode(kwargs['instance'].wiki)


class userForm(ModelForm):
    first_name = CharField(required = True, label = u"نام")
    last_name = CharField(required = True, label = u"نام خانوادگی")
    email = EmailField(label = u"رایانامه", required = True, help_text = "a@b.com")

    password = RegexField(label = u"گذر واژه", help_text = u"گذرواژه حداقل شامل 6 حرف ", widget = PasswordInput,
                          regex = "\w{6,}", error_messages = {'invalid': u"گذرواژه باید شامل حداقل 6 حرف باشد"})
    repassword = CharField(label = u"تکرار گذرواژه", widget = PasswordInput)

    is_delivery = BooleanField(label = u"حمل و نقل", required = False)
    is_wrh = BooleanField(label = u"انباردار", required = False)
    is_fnc = BooleanField(label = u"امور مالی", required = False)
    # ssn = RegexField(label=u"شماره ملی" ,regex="\d{10}",max_length=10 , error_messages={'invalid' : u"شماره ملی باید 10 رقمی باشد"})
    ssn = RegexField(label = u"شماره ملی", help_text = u"شماره ملی 10 رقمی است", regex = "\d{10}", max_length = 10,
                     error_messages = {'invalid': u"شماره ملی باید 10 رقمی باشد"})


    class Meta:
        model = User
        fields = ['username', 'password', 'repassword', 'ssn', 'first_name', 'last_name', 'email', 'is_delivery',
                  'is_fnc', 'is_wrh']


    def clean_is_wrh(self):
        print "hamedooooo"
        deliv = self.cleaned_data.get('is_delivery')
        fnc = self.cleaned_data.get('is_fnc')
        wrh = self.cleaned_data.get('is_wrh')

        if deliv == False and fnc == False and wrh == False:
            raise forms.ValidationError(u"حداقل یکی از نقش ها برای کاربر باید انتخاب شود")
        return wrh

    def clean_repassword(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('repassword')
        # password and password2 must be the same
        print( password, password2)

        if password != password2:
            raise forms.ValidationError(u"گذرواژه و تکرار ان یکسان نیست")

        return self.cleaned_data.get('password')

