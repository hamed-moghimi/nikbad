# -*- encoding: utf-8 -*-
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse_lazy

from django.db.models.aggregates import Sum
from django.shortcuts import render
from mng.views import wiki
from wiki.models import *
from django.http import *
from django.contrib.auth.decorators import login_required
from wiki.forms import *
from warehouse.models import Wiki_Order, Stock
from sales.models import SaleBill_Product, Ad


@permission_required('wiki.is_wiki', login_url = reverse_lazy('sales-index'))
def index(request):
    user = request.user.username
    wiki = Wiki.objects.filter(username = user)
    print wiki
    con = Contract.objects.filter(wiki = wiki)
    context = {'contract': con}
    return render(request, 'wiki/index.html', context)


@permission_required('wiki.is_wiki', login_url = reverse_lazy('sales-index'))
def goodsList(request):
# request.get['username']
# request.post
    if request.user.is_authenticated():
        user = request.user
        myName = user.username
        p = Product.objects.all().filter(wiki__username__iexact = myName)
        paginator = Paginator(p, 10)
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        context = {'product_list': p, 'products':products}
        return render(request, 'wiki/goodslist.html', context)


def success(request):
    return render(request, 'wiki/success.html')


def register_success(request):
    return render(request, 'wiki/register_success.html')


def product_failure(request):
    return render(request, 'wiki/productFailure.html')


def product_success(request, prod):
    context = {'product': prod}
    return render(request, 'wiki/product_success.html', context)


def register(request):
    if request.method == 'POST':
        form = WikiForm(request.POST)
        if form.is_valid():
            form.instance.set_password(form.cleaned_data['password'])
            form.save()
            wikiPerm = Permission.objects.get(codename = 'is_wiki')
            form.instance.user_permissions.add(wikiPerm)
            return register_success(request)
    else:
        form = WikiForm()
    return render(request, 'wiki/register.html', {'form': form})

def no_contract(request):
    return render(request, 'wiki/noContract.html')


def maxExceeded(request):
    return render(request, 'wiki/maxExceeded.html')

def delete_error(request, str):
    context = {'str' : str}
    return render(request, 'wiki/deleteError.html', context)

@permission_required('wiki.is_wiki', login_url = reverse_lazy('sales-index'))
def addproduct(request):
    user = request.user
    con = Contract.objects.filter(wiki__username = request.user.username)
    if con.__len__() == 0:
        return no_contract(request)
    proList = Product.objects.filter(wiki__username = request.user.username)
    if proList.__len__() == con[0].max_goods:
        return maxExceeded(request)
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
            p = Product(goodsID = gid, wiki = wiki, brand = brand,
                        name = name, sub_category = cat,
                        price = pr, off = off)
            Ad.objects.get_or_create(product = p)
            p.save()
            return product_success(request, p)
    else:
        form = ProductForm()
    return render(request, 'wiki/addProduct.html', {'form': form})


# if the requested product is in other wiki's showcase,
# you should show a message.

@permission_required('wiki.is_wiki', login_url = reverse_lazy('sales-index'))
def deleteproduct(request):
    w = Wiki.objects.filter(username = request.user.username)
    if request.method == 'POST':
        form = DeleteProductForm(request.POST)
        name = request.user.username
        if form.is_valid():

            pid = form.cleaned_data['pro']
            p = Product.objects.filter(goodsID = pid)
            if p.__len__() == 0:
                str = "no product"
                return delete_error(request, str)
            else:
                p = Product.objects.filter(goodsID = pid)[0]
                stock = Stock.objects.filter(product = p)
                if stock.__len__() > 0:
                    if stock[0].quantity == 0 and stock[0].quantity_returned == 0:
                        p.delete()
                    else:
                        str = "in wrh"
                        return delete_error(request, str)
                else:
                    str = "in wrh"
                    return delete_error(request, str)
            if p.wiki.username == name:
                p.delete()
                return success(request)
            else:
                return delete_error(request)
    else:
        form = DeleteProductForm()
    return render(request, 'wiki/deleteProduct.html', {'form': form})


@permission_required('wiki.is_wiki', login_url = reverse_lazy('sales-index'))
def wrhorders(request):
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            startDate = form.cleaned_data['startDate']
            endDate = form.cleaned_data['endDate']
            ord = Wiki_Order.objects.filter(date__range = (startDate, endDate))
            context = {'order_list': ord}
            return render(request, 'wiki/wrhorder.html', context)
    else:
        form = DateForm()
    return render(request, 'wiki/DateForm.html', {'form': form})


@permission_required('wiki.is_wiki', login_url = reverse_lazy('sales-index'))
def returnrequest(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            user = request.user
            wiki = Wiki.objects.filter(username = user.username)[0]
            date = datetime.datetime.now()
            id = form.cleaned_data['proID']
            ret = form.cleaned_data['ret_only']
            prod = Product.objects.filter(pk = id)
            if prod.__len__() == 0:
                return product_failure(request)
            p = prod[0]
            if p.wiki.username == wiki.username:
                req = ReturnRequest(wiki = wiki, pub_date = date, product = p, returned_only = ret)
                req.save()
                return success(request)
            else:
                return product_failure(request)
    else:
        form = RequestForm()
    return render(request, 'wiki/returnrequest.html', {'form': form})


@permission_required('wiki.is_wiki', login_url = reverse_lazy('sales-index'))
def salesreport(request):
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            startDate = form.cleaned_data['startDate']
            endDate = form.cleaned_data['endDate']
            list = SaleBill_Product.objects.filter(bill__saleDate__range = (startDate, endDate))
            user = request.user
            pro_list = list.filter(product__wiki__username = user.username)
            list2 = pro_list.values('product').annotate(sum = Sum('number'))
            products = []
            sums = []
            for sb in list2:
                products.append(Product.objects.get(goodsID = sb['product']))
                # print sb['sum']
                sums.append(sb['sum'])
            zipped_datea = zip(products, sums)
            context = {'pro_list': zipped_datea}
            return render(request, 'wiki/salesreport.html', context)
    else:
        form = DateForm()
    return render(request, 'wiki/DateForm.html', {'form': form})


@permission_required('wiki.is_wiki', login_url = reverse_lazy('sales-index'))
def wrhproducts(request):
    myName = request.user.username
    stock = Stock.objects.filter(product__wiki__username__iexact = myName)
    paginator = Paginator(stock, 1)
    page = request.GET.get('page')
    try:
        stocks = paginator.page(page)
    except PageNotAnInteger:
        stocks = paginator.page(1)
    except EmptyPage:
        stocks = paginator.page(paginator.num_pages)
    context = {'stock_list': stock, 'stocks' : stocks}
    return render(request, 'wiki/wrhproducts.html', context)

def editProduct(request, gId):
    p = Product.objects.get(goodsID = gId)
    if(request.POST):
        f = ProductForm(request.POST, instance = p)
        if (f.is_valid()):
            f.save()
            return product_success(request, p)
    f = ProductForm(instance = p)
    context = {'ProductForm' :f , 'p':p , 'product' : gId}
    return render(request, 'wiki/productEdit.html', context)

def contract():
    pass