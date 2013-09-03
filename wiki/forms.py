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

    companyName = CharField(label = u'نام شرکت', required = True)
    phone = RegexField(label=u"شماره تماس ",help_text="از یکی از دونمونه مقابل پیروی کنید: 02188888888 یا 09122222222",regex="\d{7,}" ,
                     error_messages={'invalid' : u"تلفن 11 رقمی است"}, required=True)
    address=CharField(widget=Textarea(),label=u"نشانی شرکت", required = True)
    password = CharField(label= u"گذر واژه", required=True, widget=PasswordInput)
    repassword = CharField(label= u"تکرار گذرواژه" ,required=True, widget=PasswordInput)
    email=EmailField(label=u"رایانامه" ,required=True ,help_text="مثال: nikbad@sarab.com"  )
    class Meta:
        model = Wiki
        fields = ['username', 'password', 'repassword','email','companyName', 'image', 'phone', 'address']


    def clean_repassword(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('repassword')
        print( password, password2)
        if password != password2:
            raise forms.ValidationError(u"گذر واژه و تکرار ان یکسان نیست")

        return self.cleaned_data.get('password')


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['goodsID','brand','name','sub_category','unit','price','off']


class DeleteProductForm(Form):
    pro = IntegerField(label=u'کدکالا', required=True)


class DateForm(Form):
    startDate = jDateField(label=u'از تاریخ ', required=True)
    endDate = jDateField(label=u' تا تاریخ', required=True)

    def clean_date(self):
        start = self.cleaned_data.get('startDate')
        end = self.cleaned_data.get('repassword')
        if start > end:
            raise forms.ValidationError(u"تاریخ وارد شده معتبر نیست. تاریخ شروع نباید از تاریخ پایان بزرگتر باشد.")
        return self.cleaned_data.get('startDate')




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

class AdminCancelForm(Form):
    wiki = ModelChoiceField(queryset=Wiki.objects.all(), empty_label=None, label="ویکی را که می خواهید قرارداد آن را فسخ کنید انتخاب کنید")



