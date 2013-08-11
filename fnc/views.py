from django.shortcuts import render
from django.http import HttpResponse
from sales.models import SaleBill
from fnc.models import *
from fnc.forms import EmployeeForm
from datetime import timedelta, datetime


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
	cb_objects = CostBenefit.objects.all()
	context = {}
	context.update({'costBenefits': cb_objects})

	sb_objects = SaleBill.objects.all()

	context.update({'saleBills': sb_objects})

	return render(request, 'fnc/gozaresh_mali.html', context)


def sabtenam_karmand(request):
	if (request.POST):
		form = EmployeeForm(request.POST)
		if (form.is_valid()):
			form.save()
			form_test = EmployeeForm(request.POST)
			context_test = {}
			context_test.update({'emp_form': form_test})
			return render(request, 'fnc/sabtenam_karmand_review.html', context_test)
	else:
		form = EmployeeForm()
	context = {}
	context.update({'emp_form': form})
	return render(request, 'fnc/sabtenam_karmand.html', context)


def karmandan(request):
	employees = Employee.objects.all()
	for ep in employees:
		rollcalls= RollCall.objects.filter(employee=ep)
		ep.hours=timedelta()
		for rc in rollcalls:
			enter= datetime.combine(rc.date,rc.entrance_time)
			exit = datetime.combine(rc.date,rc.exit_time)
			ep.hours+=enter-exit
	context = {}
	context.update({'employees': employees})
	return render(request, 'fnc/karmandan.html', context)
def karmand_detail(request,epId):
	rollcalls=RollCall.objects.filter(employee=epId)
	context = {}
	context.update({'rollcalls': rollcalls})
	return render(request, 'fnc/karmand_detail.html', context)

