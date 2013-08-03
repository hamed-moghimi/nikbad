#from build.lib.django.forms.forms import Form
from django.forms.models import ModelForm
from models import Wiki
from models import Product
from django import forms

class WikiForm(ModelForm):
    class Meta:
        model = Wiki
        fields = ['companyName','description','image','phone','address','username','password','email']

class ProductForm(ModelForm):
    class Meta:
        model = Product

class DeleteProductForm(forms.Form):
    id = forms.IntegerField(required=True )
    proname = forms.CharField(max_length=255, required=False)

