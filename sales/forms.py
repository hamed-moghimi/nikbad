# -*- coding:utf-8 -*-
from django import forms
from django.forms.forms import Form
from django.forms.widgets import Textarea, TextInput
from django.forms.models import ModelForm, BaseModelFormSet, inlineformset_factory
from models import SaleBill
from sales.models import Ad, Specification, MarketBasket_Product, AdImage
from wiki.models import Category


class SaleBillForm(ModelForm):
    class Meta:
        model = SaleBill


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