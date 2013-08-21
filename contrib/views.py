# -*- coding: utf-8 -*-

from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import password_reset
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from sales.models import MarketBasket


def login(request):
    print('login')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user is not None and user.is_active:
            auth.login(request, user)

            if user.has_perm('crm.is_customer'):
                # Customers
                return HttpResponseRedirect(reverse('sales-index'))
            elif user.has_perm('warehouse.is_warehouseman') and user.has_perm('warehouse.is_mng_warehouse'):
                # Warehouseman ke moshtarak ba manager ham dare
                return HttpResponseRedirect(reverse('warehouse-index'))
            elif user.has_perm('warehouse.is_deliveryman'):
                # Deliveryman
                return HttpResponseRedirect(reverse('warehouse-index'))
            elif user.has_perm('wiki.is_wiki'):
                # Wikis
                return HttpResponseRedirect(reverse('wiki-index'))
            elif user.has_perm('warehouse.????') or user.has_perm('warehouse.????'):
                # Warehouse admins
                return HttpResponseRedirect(reverse('warehouse-index'))
            elif user.has_perm('fnc.is_fnc'):
                # Financial admin
                return HttpResponseRedirect(reverse('fnc-index'))
            elif user.has_perm('fnc.is_manager'):
                # Manager
                return HttpResponseRedirect(reverse('manager'))

    return HttpResponseRedirect(reverse('index'))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def bank(request):
    session = request.GET['session']
    basket = MarketBasket.objects.get(pk = session)
    context = {'amount': basket.totalPrice}
    return render(request, 'contrib/bank.htm', context)