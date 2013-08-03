# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from sales.forms import SaleBillForm
from sales.models import SaleBill, Ad
from crm.models import Customer
from wiki.models import Product


def index(request):
    # get customer
    customer = Customer.objects.get(username = 'user1')
    request.user = customer

    # get new products
    new_products = Ad.objects.all()[:10]
    return render(request, 'sales/index.html', {'new_products': new_products, 'customer': customer})

def marketBasket(request):
    # get customer
    customer = Customer.objects.get(username = 'user1')
    request.user = customer

    #TODO: market basket form
    # temporary codes
    if request.method == 'POST':
        SaleBill.createFromMarketBasket(customer.marketBasket)
        customer.marketBasket.clear()
        return render(request, 'sales/success.html', {})

    return render(request, 'sales/basket.html', {'basket': customer.marketBasket})

def newBuy(request):
    #c = Customer.objects.get(username = 'user1')

    #b = SaleBill(totalPrice = 1000, customer = c)
    #b.save()
    #st = u'قبض شماره {0} در تاریخ {1} برای {2} صادر شد'.format(b.id, b.saleDate, c.get_full_name())
    form = SaleBillForm(request.POST)
    return render(request, 'sales/index.html', {'form': form})
