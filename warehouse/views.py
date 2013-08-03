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
    context = {'bills': a, 'active_menu': 3}
    return render(request, 'wrh/NewOrders.html', context)

def testback(request):
    a = SaleBill.objects.filter(deliveryStatus = 0)
    context = {'bills': a}
    return render(request, 'wrh/NewOrdersBack.html', context)

def tiny_order(request, pid):
    p2 = int(pid)
    a = SaleBill.objects.get(pk=p2)
    context = {'bill': a}
    print(a.products.all())
    return render(request, 'wrh/Tiny_Order.html', context)

def delivery_wiki_select(request):
    a = Wiki.objects.all()
    context = {'wikis': a, 'active_menu': 1}
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

def confirm_clearance(request, pid):
    p2 = int(pid)
    try:
        bill = SaleBill.objects.get(pk=p2)
        if bill.deliveryStatus == 0:
            context = {'bill': bill}
        else:
            context = {'error': "کالاهای مربوط به این سفارش قبلا از انبار خارج شده اند."}
    except Exception as e:
        context = {'error': "سفارشی با شماره داده شده یافت نشد"}
    return render(request,'wrh/ConfirmClearance.html', context)


def confirm_wrh_delivery(request):
    context = {}
    if request.method == 'POST':
        try:
            post = request.POST
            for key, value in post.iteritems():
                if key[:5]=="name_":
                    num = int(key[5:])
                    prd = Product.objects.get(pk=num)
                    stck = Stock.objects.filter(product=prd)
                    print(stck)
                    if not stck:
                        st = Stock(product=prd , quantity= value, quantity_returned=0, rack_num_returned=0, rack_num=0 )
                        st.save()
                        print(st.quantity)
                    else:
                        stck[0].quantity += int(value)
                        stck[0].save()
        except Exception as e:
            print(str(e))
    return render(request,'wrh/ConfirmationWRHDelivery.html', context)

def clearance(request):
    context = { 'active_menu': 2}
    return render(request,'wrh/Clearance.html', context)

def clearance2(request):
    context = { 'active_menu': 2}
    return render(request,'wrh/Clearance2.html', context)

def clear_end(request, pid):
    context = {}
    p2 = int(pid)
    bill = SaleBill.objects.get(pk = p2)
    bill.deliveryStatus = 1
    bill.save()
    return render(request,'wrh/ConfirmClearance-end.html', context)