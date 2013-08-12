__author__ = 'Roya'

# -*- encoding: utf-8 -*-
from wiki.models import Contract
from django.forms.models import ModelForm

class ContractForm(ModelForm):
    class Meta:
        model = Contract

