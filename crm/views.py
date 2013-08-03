from django.shortcuts import render
from django.http import HttpResponse
from django.template import context
from crm.forms import CustomerForm
from sales.models import SaleBill
from crm.models import *


def index(request):
    f = CustomerForm(request.POST)
    return render(request, 'crm/base.html', {'CustomerForm' : f})

def edit(request):
    f = CustomerForm(request.POST)
    return render(request, 'crm/edit.html', {'CustomerForm' : f})

def signUp(request):
    if(request.POST):
        f = CustomerForm(request.POST)
        if (f.is_valid()):
            f.save()
            return success(request)
    else:
        f = CustomerForm()
    return render(request, 'crm/signUp.html', {'CustomerForm' : f})


def status(request):
    c = Customer.objects.all()[0]
    sb = c.saleBills.all()[0]
    p =  sb.products.all()
    print ("bill ")
    print sb
    context = { 'Product' : p , 'Bill' : sb }
    return render(request, 'crm/status.html', context)

def success(request):
    f = CustomerForm(request.POST)
    return render(request, 'crm/signUp-successful.html', {'CustomerForm' : f})

def index2(request):
    #request.get['username']
    #request.post
    #l = SaleBill.objects.all()[0]
    #return HttpResponse('{0} and {1} and {2}'.format(l.saleDate, l.totalPrice, l.costumer.balance))
    return render(request, 'base.html', {})
