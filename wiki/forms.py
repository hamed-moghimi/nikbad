# -*- encoding: utf-8 -*-

# from build.lib.django.forms.forms import Form
from cProfile import label
from django.db.models.fields import CharField, PositiveSmallIntegerField, PositiveIntegerField
from django.forms.models import ModelForm
from contrib.forms import jDateField
from models import Wiki
from models import *
from django.forms import *

class WikiForm(ModelForm):

    password = CharField(label= u"گذر واژه" ,widget=PasswordInput)
    repassword = CharField(label= u"تکرار گذرواژه" ,widget=PasswordInput)

    class Meta:
        model = Wiki
        fields = ['companyName', 'image', 'phone', 'address', 'username', 'password', 'repassword','email']

        def clean_phone(self):
            phone = self.cleaned_data.get('phone')
            if phone.__len__ < 8 or phone.__len__ > 11:
                raise forms.ValidationError(u'شماره تلفن داده شده معتبر نیست')


    def clean_repassword(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('repassword')
        print( password, password2)
        if password != password2:
            raise forms.ValidationError(u"گذر واژه و تکرار ان یکسان نیست")


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['goodsID','brand','name','sub_category','price','off']


class DeleteProductForm(Form):
    pro = IntegerField(label=u'کدکالا')


class DateForm(Form):
    startDate = jDateField(label=u'از تاریخ ')
    endDate = jDateField(label=u' تا تاریخ')




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

class RequestForm(Form):
    proID = IntegerField(label=u'کد کالا')
    ret_only = NullBooleanField(label=u'فقط کالاهای بازگشتی را بازگردان')

class ConRequestForm(Form):
    abonne = IntegerField(label=u'مبلغ آبونمان پیشنهادی برای هر ماه(ریال)')
    benefit = IntegerField(label=u'درصد کارمزد پیشنهادی سراب به ازای هر کالا')

class ConCancelForm(ModelForm):
    class Meta:
        model = ConCancel
        fields = []





