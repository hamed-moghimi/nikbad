from django.shortcuts import render
from django.http import HttpResponse
from django.template import context
from sales.models import SaleBill
from crm.models import *


def index(request):
    #request.get['username']
    #request.post
    #l = SaleBill.objects.all()[0]
    #return HttpResponse('{0} and {1} and {2}'.format(l.saleDate, l.totalPrice, l.costumer.balance))
    return render(request, 'crm/base.html', {})

def edit(request):
    #request.get['username']
    #request.post
    #l = SaleBill.objects.all()[0]
    #return HttpResponse('{0} and {1} and {2}'.format(l.saleDate, l.totalPrice, l.costumer.balance))
    return render(request, 'crm/edit.html', {})
def signUp(request):
    #request.get['username']
    #request.post
    #l = SaleBill.objects.all()[0]
    #return HttpResponse('{0} and {1} and {2}'.format(l.saleDate, l.totalPrice, l.costumer.balance))
    return render(request, 'crm/signUp.html', {})
def status(request):
    c = Customer.objects.all()[0]
    s = SaleBill.get().filter(Customer=c)
    sb = c.saleBills
    context = { 'Product' : p }
    return render(request, 'crm/status.html', context)

def success(request):
    #request.get['username']
    #request.post
    #l = SaleBill.objects.all()[0]
    #return HttpResponse('{0} and {1} and {2}'.format(l.saleDate, l.totalPrice, l.costumer.balance))
    return render(request, 'crm/signUp-successful.html', {})

def index2(request):
    #request.get['username']
    #request.post
    #l = SaleBill.objects.all()[0]
    #return HttpResponse('{0} and {1} and {2}'.format(l.saleDate, l.totalPrice, l.costumer.balance))
    return render(request, 'base.html', {})
