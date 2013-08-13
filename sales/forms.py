from django.forms.models import ModelForm, BaseModelFormSet, inlineformset_factory
from models import SaleBill
from sales.models import Ad, Specification


class SaleBillForm(ModelForm):
    class Meta:
        model = SaleBill


class AdForm(ModelForm):
    class Meta:
        model = Ad
        exclude = ['icon', 'product']