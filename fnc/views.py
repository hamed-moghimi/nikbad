from django.shortcuts import render
from django.http import HttpResponse
from sales.models import SaleBill
from fnc.models import *
from fnc.forms import EmployeeForm


def index(request):
	#request.get['username']
	#request.post
	#l = SaleBill.objects.all()[0]
	#return HttpResponse('{0} and {1} and {2}'.format(l.saleDate, l.totalPrice, l.costumer.balance))
	return render(request, 'fnc/base.html', {})


def gozaresh_mali(request):
#request.get['username']
#request.post
#l = SaleBill.objects.all()[0]
#return HttpResponse('{0} and {1} and {2}'.format(l.saleDate, l.totalPrice, l.costumer.balance))
	cb_objects= CostBenefit.objects.all()
	context={}
	context.update({'costBenefits':cb_objects})

	sb_objects=SaleBill.objects.all()

	context.update({'saleBills':sb_objects})

	return render(request, 'fnc/gozaresh_mali.html', context)
def sabtenam_karmand(request):
	if(request.POST):
		form = EmployeeForm(request.POST)
		if(form.is_valid()):
			form.save()
			form_test = ItemForm()
			context_test={}
			context_test.update({'emp_form':form_test})
			return render(request,'fnc/sabtenam_karmand_review.html', context_test)
	else:
		form = EmployeeForm()
	context={}
	context.update({'emp_form':form})
	return render(request, 'fnc/sabtenam_karmand.html', context)

class ItemForm(EmployeeForm):
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['sku'].widget.attrs['readonly'] = True

    def clean_sku(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.sku
        else:
            return self.cleaned_data['sku']