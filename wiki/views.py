# -*- encoding: utf-8 -*-

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from wiki.models import *
from django.http import *
from django.contrib.auth.decorators import login_required
from wiki.forms import *


@login_required
def goodsList(request):
#request.get['username']
#request.post

    if request.user.is_authenticated():
        user = request.user
        myName = user.username
        #print user
        # p = Product.objects.all().filter(wiki__username__iexact=myName)
        p = Product.objects.filter(wiki__companyName = u'سیب')
        context = {'product_list': p}
        return render(request, 'wiki/goodslist.html', context)

def success(request):
    return render(request, 'wiki/success.html')

def product_failure(request):
    return render(request, 'wiki/productFailure.html')


def register(request):
    if request.method == 'POST':
        form = WikiForm(request.POST)
    # st = u'ثبت نام با موفقیت انجام شد.'
        if form.is_valid():
            un = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            cn = form.cleaned_data['companyName']
            desc = form.cleaned_data['description']
            ph = form.cleaned_data['phone']
            ad = form.cleaned_data['address']
            em = form.cleaned_data['email']
            w = Wiki(username = un, password = pw,
                     companyName = cn, description = desc,
                     phone = ph, address = ad, email = em)
            w.save()
            return success(request)
    else:
        form = WikiForm()
    return render(request, 'wiki/register.html', {'form': form})


def addProduct(request):

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            print 'hello'
            gid = form.cleaned_data['goodsID']
            wiki = form.cleaned_data['wiki']
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
def deleteProduct(request):
    if request.method == 'POST':
        form = DeleteProductForm(request.POST)
        if form.is_valid():
            print 'salam'
            pid = form.cleaned_data['id']
            name = form.cleaned_data['proname']
            p = Product.objects.filter(goodsID = pid)
            if (p.__len__() == 0):
                return product_failure(request)
            p.delete()
            return success(request)
    else:
        form = DeleteProductForm()
    return render(request, 'wiki/deleteProduct.html', {'form': form})
