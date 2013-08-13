# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse_lazy

from django.db.models.aggregates import Sum
from django.shortcuts import render
from mng.views import wiki
from wiki.models import *
from django.http import *
from django.contrib.auth.decorators import login_required
from wiki.forms import *
from warehouse.models import Wiki_Order, Stock
from sales.models import SaleBill_Product


@permission_required('wiki.is_wiki', login_url = reverse_lazy('sales-index'))
def index(request):
    user = request.user.username
    wiki = Wiki.objects.filter(username = user)
    print wiki
    con = Contract.objects.filter(wiki = wiki)
    context = {'contract' : con}
    return render(request, 'wiki/index.html', context)

@permission_required('wiki.is_wiki', login_url = reverse_lazy('wiki-index'))
def goodsList(request):
# request.get['username']
# request.post
    if request.user.is_authenticated():
        user = request.user
        myName = user.username
        p = Product.objects.all().filter(wiki__username__iexact=myName)

        context = {'product_list': p}
        return render(request, 'wiki/goodslist.html', context)

def success(request):
    return render(request, 'wiki/success.html')

def register_success(request):
    return render(request, 'wiki/register_success.html')

def product_failure(request):
    return render(request, 'wiki/productFailure.html')

def product_success(request):
    return render(request, 'wiki/product_success.html')

def register(request):
    pass
    if request.method == 'POST':
         form = WikiForm(request.POST)
         if form.is_valid():
             form.save()
             return register_success(request)
    else:
         form = WikiForm()
    return render(request, 'wiki/register.html', {'form': form})

@permission_required('wiki.is_wiki', login_url = reverse_lazy('wiki-index'))
def addproduct(request):
    user = request.user
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            print 'hello'
            gid = form.cleaned_data['goodsID']
            wiki = Wiki.objects.filter(username = user.username)[0]
            brand = form.cleaned_data['brand']
            name = form.cleaned_data['name']
            cat = form.cleaned_data['sub_category']
            pr = form.cleaned_data['price']
            off = form.cleaned_data['off']
            p = Product(goodsID=gid, wiki=wiki, brand=brand,
                        name=name, sub_category=cat,
                        price=pr, off=off)
            p.save()
            return success(request)
    else:
        form = ProductForm()
    return render(request, 'wiki/addProduct.html', {'form': form})



# if the requested product is in other wiki's showcase,
    # you should show a message.

@permission_required('wiki.is_wiki', login_url = reverse_lazy('wiki-index'))
def deleteproduct(request):
    if request.method == 'POST':
        form = DeleteProductForm(request.POST)
        name  = request.user.username
        if form.is_valid():
            print 'salam'
            pid = form.cleaned_data['id']
            name = form.cleaned_data['proname']
            p = Product.objects.filter(goodsID = pid)
            if p.__len__() == 0:
                return product_failure(request)
            if p.wiki.username == name:
                p.delete()
                return success(request)
    else:
        form = DeleteProductForm()
    return render(request, 'wiki/deleteProduct.html', {'form': form})

@permission_required('wiki.is_wiki', login_url = reverse_lazy('wiki-index'))
def wrhorders(request):
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            startDate = form.cleaned_data['startDate']
            endDate = form.cleaned_data['endDate']
            ord = Wiki_Order.objects.filter(date__range=(startDate, endDate))
            context = {'order_list': ord}
            return render(request, 'wiki/wrhorder.html', context)
    else:
        form = DateForm()
    return render(request, 'wiki/DateForm.html', {'form' : form})

@permission_required('wiki.is_wiki', login_url = reverse_lazy('wiki-index'))
def returnrequest(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            user = request.user
            wiki = Wiki.objects.filter(username = user.username)[0]
            date = datetime.datetime.now()
            id = form.cleaned_data['proID']
            ret = form.cleaned_data['ret_only']
            prod = Product.objects.filter(pk=id)
            if prod.__len__() == 0:
                return product_failure(request)
            p = prod[0]
            if p.wiki.username == wiki.username :
                req = ReturnRequest(wiki = wiki, pub_date = date, product = p, returned_only = ret)
                req.save()
                return success(request)
            else:
                return product_failure(request)
    else:
        form = RequestForm()
    return render(request, 'wiki/returnrequest.html', {'form': form})

@permission_required('wiki.is_wiki', login_url = reverse_lazy('wiki-index'))
def salesreport(request):

    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            startDate = form.cleaned_data['startDate']
            endDate = form.cleaned_data['endDate']
            pro_list = SaleBill_Product.objects.filter(bill__saleDate__range = (startDate, endDate))
            user = request.user

            list2 = pro_list.values('product').annotate(sum=Sum('number'))
            products = []
            sums = []
            for sb in list2:
                products.append(Product.objects.get(goodsID = sb['product']))
                # print sb['sum']
                sums.append(sb['sum'])
            zipped_datea = zip(products,sums)
            context = {'pro_list': zipped_datea}
            return render(request, 'wiki/salesreport.html', context)
    else:
        form = DateForm()
    return render(request, 'wiki/DateForm.html', {'form' : form})


@permission_required('wiki.is_wiki', login_url = reverse_lazy('wiki-index'))
def wrhproducts(request):
    myName = request.user.username
    stock = Stock.objects.filter(product__wiki__username__iexact=myName)
    context = {'stock_list': stock}
    return render(request, 'wiki/wrhproducts.html', context)
