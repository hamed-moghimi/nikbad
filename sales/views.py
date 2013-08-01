from django.shortcuts import render
from django.http import HttpResponse
from sales.models import SaleBill
from fnc.models import CostBenefit


def index(request):
    #request.get['username']
    #request.post
	l = SaleBill.objects.all()[0]
	cost_benefit_objects= CostBenefit.objects.all()
	return render(request, 'sales/index.html', {})
    #return HttpResponse('{0} and {1} and {2}'.format(l.saleDate, l.totalPrice, l.costumer.balance))


def index2(request):
    #request.get['username']
    #request.post
    #l = SaleBill.objects.all()[0]
    #return HttpResponse('{0} and {1} and {2}'.format(l.saleDate, l.totalPrice, l.costumer.balance))
    return render(request, 'base.html', {})