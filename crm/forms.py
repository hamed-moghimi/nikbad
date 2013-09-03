#-*- coding:utf-8 -*-
from django.forms.models import ModelForm
from crm.models import Customer
from django.forms import *

class checkCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['username' , 'first_name', 'last_name', 'gender' , 'phone'  , 'email'  , 'postal_code', 'city' , 'address' ]


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


class CustomerForm(ModelForm):
    password = RegexField(label= u"گذر واژه" ,help_text=u"گذرواژه حداقل شامل 6 حرف ",widget=PasswordInput,regex="\w{6,}" , error_messages={'invalid' : u"گذرواژه باید شامل حداقل 6 حرف باشد"})
    repassword = CharField(label= u"تکرار گذرواژه" ,widget=PasswordInput)
    first_name=CharField(required=True ,label=u"نام" )
    last_name=CharField(required=True ,label=u"نام خانوادگی" )
    postal_code=RegexField(label=u"کدپستی",help_text=u"کدپستی ده رقمی است",required=True,regex="\d{10}" , error_messages={'invalid' : u"کدپستی شامل 10 رقم است"})
    email=EmailField(label=u"رایانامه" ,required=True ,help_text="یک رایانامه معتبر مثل: nikbad@sarab.com")
    phone=RegexField(label=u"شماره تماس ثابت",help_text="تلفن به همراه کد شهرستان 11 رقمی می باشد مثل:0218826299",regex="\d{7,}" , error_messages={'invalid' : u"تلفن ثابت 11 رقمی است"})
    address=CharField(widget=Textarea(),label=u"نشانی محل سکونت")
    # username=RegexField(label=u"نام کاربری" , help_text=u"حداکثر 30 حرف شامل ارقام و حروف الفبا")
    class Meta:
        model = Customer
        fields = ['username','password','repassword' , 'first_name', 'last_name' , 'phone'  , 'email'  , 'postal_code', 'city' , 'address' ]


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


