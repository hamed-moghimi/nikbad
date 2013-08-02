# -*- encoding: utf-8 -*-
from operator import pos
from django.shortcuts import render
from sales.models import SaleBill
from wiki.models import *
from warehouse.models import *

def index(request):
    a = u'سامانه انار'
    context = {'name': a}
    return render(request, 'wrh/base.html', context)

def test(request):
    a = SaleBill.objects.filter(deliveryStatus = 0)
    context = {'bills': a}
    return render(request, 'wrh/NewOrders.html', context)

def testback(request):
    a = SaleBill.objects.filter(deliveryStatus = 0)
    context = {'bills': a}
    return render(request, 'wrh/NewOrdersBack.html', context)

def tiny_order(request, pid):
    a = SaleBill.objects.get(pk=pid)
    context = {'bill': a}
    return render(request, 'wrh/Tiny_Order.html', context)

def delivery_wiki_select(request):
    a = Wiki.objects.all()
    context = {'wikis': a}
    return render(request,'wrh/WRHDelivery.html', context)

def delivery_wiki_select2(request):
    a = Wiki.objects.all()
    context = {'wikis': a}
    return render(request,'wrh/WRHDelivery2.html', context)


def delivery_product_select(request, pid):
    wik = Wiki.objects.filter(pk=pid)
    a = Product.objects.filter(wiki=wik)
    context = {'products': a}
    return render(request,'wrh/WRHDelivery-next.html', context)

def confirm_wrh_delivery(request):
    context = {}
    if request.method == 'POST':
        try:
            post = request.POST
            for key, value in post.iteritems():
                num = int(key)
                prd = Product.objects.get(pk=num)
                stck = Stock.objects.filter(product=prd)
                if stck:
                    stck[0].quantity += value
                    context = {'st': stck[0], 'value': value+2}
                    stck[0].save()
                else:
                    Stock.objects.create(product=prd, quantity=value)
                    st = Stock.objects.get(product=prd)
                    context = {'st': st ,'value': value}
        except:
            context.update({'error': u'اطلاعات وارد شده نشان دهنده یک فرم کامل نیست.'})
    return render(request,'wrh/ConfirmationWRHDelivery.html', context)