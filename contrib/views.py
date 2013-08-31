# -*- coding: utf-8 -*-

from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import password_reset
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.shortcuts import render
import time
from sales.models import MarketBasket


def login(request):
    if request.method == 'POST':
        if request.is_ajax():
            ResponseType = HttpResponse
        else:
            ResponseType = HttpResponseRedirect

        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user is not None and user.is_active:
            auth.login(request, user)

            if user.has_perm('crm.is_customer'):
                # Customers
                return ResponseType(reverse('sales-index'))
            elif user.has_perm('warehouse.is_warehouseman') and user.has_perm('warehouse.is_mng_warehouse'):
                # Warehouseman ke moshtarak ba manager ham dare
                return ResponseType(reverse('warehouse-index'))
            elif user.has_perm('warehouse.is_deliveryman'):
                # Deliveryman
                return ResponseType(reverse('warehouse-index'))
            elif user.has_perm('wiki.is_wiki'):
                # Wikis
                return ResponseType(reverse('wiki-index'))
            elif user.has_perm('fnc.is_fnc'):
                # Financial admin
                return ResponseType(reverse('fnc-index'))
            elif user.has_perm('fnc.is_manager'):
                # Manager
                return ResponseType(reverse('manager'))

    return HttpResponseForbidden(u'نام کاربری یا رمز عبور اشتباه است.')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def bank(request):
    session = request.GET['session']
    basket = MarketBasket.objects.get(pk = session)
    context = {'amount': basket.totalPrice}
    return render(request, 'contrib/bank.htm', context)


def error_handler(request):
    return render(request, 'error_page.html', {})