from django.shortcuts import render
from django.http import HttpResponse
from sales.models import SaleBill
from fnc.models import *
# from fnc.forms import EmployeeForm


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
	return render(request, 'fnc/gozaresh_mali.html', context)
def sabtenam_karmand(request):
	context={}
	# form = EmployeeForm()
	# context.update({'emp_form':form})
	return render(request, 'fnc/sabtenam_karmand.html', context)