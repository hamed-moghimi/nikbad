from django.forms.models import ModelForm
from models import SaleBill

class SaleBillForm(ModelForm):
    class Meta:
        model = SaleBill