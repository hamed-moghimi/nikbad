from django.shortcuts import render
from django.http import HttpResponse
from sales.models import SaleBill


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
	context = {'a': 6, 'd': 9}
	context.update({'f': 0})
	return render(request, 'gozaresh_mali.html', context)