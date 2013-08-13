#from Demos.win32ts_logoff_disconnected import *
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import encoding
from crm.forms import CustomerForm, EditForm, checkCustomerForm

from crm.models import *
from sales.models import MarketBasket


def index(request):
    print request.user.username
    c = Customer.objects.get(username = request.user.username)
    print("here  sdsd" + c.username)
    f = EditForm(instance = c)
    # if (f.is_valid()):
    # f.save()
    print "saveeeeeeeeeeeeeeeeed"
    sb = c.saleBills.all()[0]
    p = sb.products.all()
    context = {'Product': p, 'Bill': sb, 'EditForm': f}

    return render(request, 'crm/base.html', context)


def edit(request):
    c = Customer.objects.get(username = request.user.username)
    if (request.POST):
        f = EditForm(request.POST, instance = c)
        if (f.is_valid()):
            f.save()
            print " khhhhhhhhhhhhhhhhhhhhhhhhh"
            return edit_success(request)
    f = EditForm(instance = c)
    # else :
    #     print "intoooooooooooooooo"
    return render(request, 'crm/edit.html', {'EditForm': f})


def signUp(request):
    if (request.POST):
        f = CustomerForm(request.POST)
        if (f.is_valid()):
            f.instance.set_password(f.cleaned_data['password'])
            f.save()
            MarketBasket.createForCustomer(f.instance)
            return success(request)
    else:
        f = CustomerForm()
    return render(request, 'crm/signUp.html', {'CustomerForm': f})


@permission_required('crm.is_customer', login_url = reverse_lazy('sales-index'))
def status(request):
    c = Customer.objects.get(username = request.user.username)
    sb = c.saleBills.all()[0]
    p = sb.products.all()

    context = {'Product': p, 'Bill': sb}
    return render(request, 'crm/status.html', context)


def success(request):
    f = checkCustomerForm(request.POST)
    return render(request, 'crm/signUp-successful.html', {'checkCustomerForm': f})


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
