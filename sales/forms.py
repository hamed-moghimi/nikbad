from django import forms
from django.forms.widgets import Textarea
from django.forms.models import ModelForm, BaseModelFormSet, inlineformset_factory
from models import SaleBill
from sales.models import Ad, Specification, MarketBasket_Product


class SaleBillForm(ModelForm):
    class Meta:
        model = SaleBill


class AdForm(ModelForm):
    description = forms.CharField(widget = Textarea(attrs = {'class': 'input-block-level'}))

    class Meta:
        model = Ad
        fields = ['description']


class MBPForm(ModelForm):
    class Meta:
        model = MarketBasket_Product
        fields = ['number']