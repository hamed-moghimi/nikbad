# -*- encoding:utf-8 -*-
#from Demos.win32ts_logoff_disconnected import *
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import encoding
from contrib.email import render_and_email
from crm.forms import CustomerForm, EditForm, checkCustomerForm, DateForm
from crm.models import *
from sales.models import MarketBasket


@permission_required('crm.is_customer', login_url = reverse_lazy('sales-index'))
def index(request):
    print request.user.username
    c = Customer.objects.get(username = request.user.username)
    print("here  sdsd" + c.username)
    f = EditForm(instance = c)
    # if (f.is_valid()):
    # f.save()
    print "saveeeeeeeeeeeeeeeeed"
    sb = []
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            startDate = form.cleaned_data['startDate']
            endDate = form.cleaned_data['endDate']
            sb = c.saleBills.objects.filter(date__range = (startDate, endDate))

    try:
        # sb = c.saleBills.all()[0]
        p = sb.products.all()
        context = {'Product': p, 'Bill': sb, 'EditForm': f}
    except:
        context = {'EditForm': f}
    return render(request, 'crm/base.html', context)


@permission_required('crm.is_customer', login_url = reverse_lazy('sales-index'))
def edit(request):
    c = Customer.objects.get(username = request.user.username)
    if (request.POST):
        f = EditForm(request.POST, instance = c)
        try:
            request.POST['gender'] = request.POST['gender'].encode('utf-8')
        except:
            pass
        if (f.is_valid()):
            f.save()
            print " khhhhhhhhhhhhhhhhhhhhhhhhh"
            return edit_success(request)
    f = EditForm(instance = c)
    # else :
    #     print "intoooooooooooooooo"
    return render(request, 'crm/edit.html', {'EditForm': f})


def signUp(request):
    is_customer = Permission.objects.get(codename = 'is_customer')
    if (request.POST):
        f = CustomerForm(request.POST)
        if (f.is_valid()):
            f.instance.set_password(f.cleaned_data['password'])
            f.save()
            f.instance.user_permissions.add(is_customer)

            MarketBasket.createForCustomer(f.instance)
            # name = f.instance.Get['first_name']
            # ren
            context = {'first_name': f.cleaned_data['first_name'], 'last_name': f.cleaned_data['last_name']}

            render_and_email([f.cleaned_data['email']], u'ثبت کاربر جدید', u"عضو شدید", 'crm/signUp_email.html',
                             context)
            return success(request)
    else:
        f = CustomerForm()
    return render(request, 'crm/signUp.html', {'CustomerForm': f})


@permission_required('crm.is_customer', login_url = reverse_lazy('sales-index'))
def status(request):
    c = Customer.objects.get(username = request.user.username)
    # sb = []
    # if request.method == 'POST':
    #     form = DateForm(request.POST)
    #     if form.is_valid():
    #         startDate = form.cleaned_data['startDate']
    #         endDate = form.cleaned_data['endDate']
    #         sb = c.saleBills.objects.filter(date__range = (startDate, endDate))
    #
    # try:
    #     p = sb.products.all()
    #     context = {'Product': p, 'Bill': sb}
    # except:
    #     context = {}


    sb = []
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            startDate = form.cleaned_data['startDate']
            endDate = form.cleaned_data['endDate']
            sb = c.saleBills.objects.filter(date__range = (startDate, endDate))

    try:
        # sb = c.saleBills.all()[0]
        p = sb.products.all()
        context = {'Product': p, 'Bill': sb}
    except:
        context = {}
        # context = {'Product': p, 'Bill': sb}
    return render(request, 'crm/status.html', context)


# @permission_required('crm.is_customer', login_url = reverse_lazy('sales-index'))
def success(request):
    f = checkCustomerForm(request.POST)
    return render(request, 'crm/signUp-successful.html', {'checkCustomerForm': f})


@permission_required('crm.is_customer', login_url = reverse_lazy('sales-index'))
def edit_success(request):
    f = EditForm(request.POST)
    return render(request, 'crm/edit-successful.html', {'EditForm': f})


@permission_required('crm.is_customer', login_url = reverse_lazy('sales-index'))
def feedback(request):
    try:
        if (request.POST and request.is_ajax()):
            f = Feedback()
            f.content = request.POST['content'].encode('utf-8')
            c = Customer.objects.get(username = request.user.username)
            f.Customer = c
            f.product_id = int(request.POST['productID'])
            f.save()
            return HttpResponse("ok")
        else:
            return HttpResponseForbidden()
    except:
        return HttpResponseForbidden()
