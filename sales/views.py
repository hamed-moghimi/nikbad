# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from sales.forms import SaleBillForm
from sales.models import SaleBill
from crm.models import Customer


def index(request):
    #request.get['username']
    #request.post
    #l = SaleBill.objects.all()[0]
    #return HttpResponse('{0} and {1} and {2}'.format(l.saleDate, l.totalPrice, l.costumer.balance))
    return render(request, 'sales/index.html', {})

def newBuy(request):
    c = Customer.objects.get(username = 'user1')
    b = SaleBill(totalPrice = 1000, customer = c)
    b.save()
    st = u'قبض شماره {0} در تاریخ {1} برای {2} صادر شد'.format(b.id, b.saleDate, c.get_full_name())
    form = SaleBillForm(request.POST)
    return render(request, 'sales/index.html', {'message': st, 'form': form})

def index2(request):
    #request.get['username']
    #request.post
    #l = SaleBill.objects.all()[0]
    #return HttpResponse('{0} and {1} and {2}'.format(l.saleDate, l.totalPrice, l.costumer.balance))
    return render(request, 'base.html', {})
