# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from sales.forms import SaleBillForm
from sales.models import SaleBill, Ad, AdImage, MarketBasket
from crm.models import Customer
from wiki.models import Product

def createNewAds():
    print('salam')
    pl = Product.objects.all()
    for p in pl:
        a, ok = Ad.objects.get_or_create(product = p, description = u'اجناس خوب و مرغوب')
        icon = AdImage.objects.create(ad = a, title = u'تصویر', image = '/media/ad_images/{0}.jpg'.format(a.id))
        a.icon = icon
        a.save()

def index(request):
    # get customer
    customer = request.user
    try:
        customer = Customer.objects.get(username = request.user.username)
        request.user = customer
        mb, ok = MarketBasket.objects.get_or_create(customer = customer)
        mb.items.get_or_create(product = Product.objects.all()[0], number = 3)
        customer.marketBasket = mb
        customer.save()
    except:
        pass
    createNewAds()
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


def index2(request):
    return render(request, 'sales/index.html', {})