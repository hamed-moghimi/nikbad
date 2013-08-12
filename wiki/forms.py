# -*- encoding: utf-8 -*-

# from build.lib.django.forms.forms import Form

from django.db.models.fields import CharField
from django.forms.models import ModelForm
from models import Wiki
from models import *
from django.forms import *
from django.forms.extras.widgets import SelectDateWidget

class WikiForm(ModelForm):

    password = CharField(label= u"گذر واژه" ,widget=PasswordInput)
    repassword = CharField(label= u"تکرار گذرواژه" ,widget=PasswordInput)

    class Meta:
        model = Wiki
        fields = ['companyName', 'description', 'image', 'phone', 'address', 'username', 'password', 'repassword','email']


def clean_repassword(self):
    password = self.cleaned_data.get('password')
    password2 = self.cleaned_data.get('repassword')
    print( password, password2)
    if password != password2:
        raise forms.ValidationError(u"گذر واژه و تکرار ان را یکسان نیست")


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['goodsID','brand','name','unit','volume','cat','sub_category','price','off']


class DeleteProductForm(Form):
    id = IntegerField(label=u'کد کالا', required=True)
    proname = CharField(label=u'نام کالا',max_length=255, required=False)

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

class RequestForm(Form):
    proID = IntegerField(label=u'کد کالا')
    ret_only = BooleanField(label=u'فقط کالاهای بازگشتی را بازگردان')





