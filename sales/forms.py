# -*- coding:utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from django.forms.fields import IntegerField
from django.forms.forms import Form
from django.forms.widgets import Textarea, TextInput
from django.forms.models import ModelForm, BaseModelFormSet, inlineformset_factory
from contrib.forms import NumberInput
from models import SaleBill
from sales.models import Ad, Specification, MarketBasket_Product, AdImage
from wiki.models import Category


class SaleBillForm(ModelForm):
    class Meta:
        model = SaleBill


class MBFrom(ModelForm):
    number = IntegerField(widget = NumberInput(attrs = {'min': 1, 'max': 30, 'class': 'span1'}))

    class Meta:
        model = MarketBasket_Product

    def clean_number(self):
        if self.cleaned_data['product'].stock_set.all()[0].enough_stock(self.cleaned_data['number']):
            return self.cleaned_data['number']

        self.fields['number'].widget.attrs.update({'class': 'span1 error'})
        raise ValidationError(u'موجودی محصول کافی نیست.')


class AdForm(ModelForm):
    description = forms.CharField(widget = Textarea(attrs = {'class': 'input-block-level'}))

    class Meta:
        model = Ad
        fields = ['description']


class AdImageForm(ModelForm):
    title = forms.CharField(required = False)
    image = forms.ImageField(required = False, widget = forms.FileInput)

    class Meta:
        model = AdImage
        fields = ['title', 'image']


class SearchForm(Form):
    query = forms.CharField(required = False, widget = TextInput(
        attrs = {'class': "search-query input-medium", 'placeholder': "جستجو ..."}))
    category = forms.ModelChoiceField(Category.objects.all(), empty_label = u'همه موارد', required = False)