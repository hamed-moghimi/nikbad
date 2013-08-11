# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from sales.forms import SaleBillForm
from sales.models import SaleBill, Ad, AdImage, MarketBasket
from crm.models import Customer
from wiki.models import Product

def createNewAds():
    pl = Product.objects.all()
    for p in pl:
        a, ok = Ad.objects.get_or_create(product = p, description = u'اجناس خوب و مرغوب')
        icon = AdImage.objects.create(ad = a, title = u'تصویر', image = '/media/ad_images/{0}.jpg'.format(a.id))
        a.icon = icon
        a.save()

# @user_passes_test(customer bashad?! :D)
def index(request):
    customer = request.user
    print(customer.user_permissions.all())
    # get customer
    try:
        customer = Customer.objects.get(username = request.user.username)
        if customer.is_active:
            request.user = customer
        else:
            raise None
    except:
        request.user = customer = None

    # get new products
    new_products = Ad.objects.all()[:10]

    # get popular products
    populars = Ad.objects.all()[:10] #order_by('-popularity')[:10]
    return render(request, 'sales/index.html', {'new_products': new_products, 'populars': populars, 'customer': customer})

def category(request, catID):

    catID = int(catID)

    # get customer
    customer = request.user
    try:
        customer = Customer.objects.get(username = request.user.username)
        if customer.is_active:
            request.user = customer
        else:
            raise None
    except:
        request.user = customer = None

    # get new products
    new_products = Ad.objects.all() #filter(subCategory__category__id = catID)[:10]

    # get popular products
    populars = Ad.objects.all() #filter(subCategory__category__id = catID)[:10] #order_by('-popularity')[:10]
    return render(request, 'sales/index.html', {'new_products': new_products, 'populars': populars, 'customer': customer, 'category': catID})


def detailsPage(request, itemCode):
    # get customer
    customer = request.user
    try:
        customer = Customer.objects.get(username = request.user.username)
        if customer.is_active:
            request.user = customer
        else:
            raise None
    except:
        request.user = customer = None

    try:
        ad = Ad.objects.get(id = itemCode)
    except:
        return HttpResponseRedirect(reverse('sales-index'));

    return render(request, 'sales/details.html', {'item': ad, 'customer': customer})


@permission_required('crm.is_customer', login_url=reverse_lazy('sales-index'))
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