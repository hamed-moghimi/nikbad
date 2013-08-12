#from Demos.win32ts_logoff_disconnected import *
from django.shortcuts import render
from django.http import HttpResponse
from crm.forms import CustomerForm,EditForm

from crm.models import *


def index(request):
    print request.user.username
    c = Customer.objects.get(username=request.user.username)
    print("here  sdsd"+ c.username)
    f = EditForm( instance=c )
    # if (f.is_valid()):
    # f.save()
    print "saveeeeeeeeeeeeeeeeed"
    sb = c.saleBills.all()[0]
    p =  sb.products.all()
    context = { 'Product' : p , 'Bill' : sb , 'EditForm' : f}

    return render(request, 'crm/base.html', context)

def edit(request):
    # f = CustomerForm(request.POST)
    c = Customer.objects.get(username=request.user.username)
    f = CustomerForm( instance=c )

    # c = Customer.objects.all()[0]
    sb = c.saleBills.all()[0]
    p =  sb.products.all()
    context = { 'Product' : p , 'Bill' : sb }
    return render(request, 'crm/edit.html', {'CustomerForm' : f})

def signUp(request):
    if(request.POST):
        f = CustomerForm(request.POST)
        if (f.is_valid()):
            f.save()
            return success(request)
    else:
        f = CustomerForm()
    return render(request, 'crm/signUp.html', {'CustomerForm' : f})


def status(request):
    c = Customer.objects.all()[0]
    sb = c.saleBills.all()[0]
    p =  sb.products.all()

    context = { 'Product' : p , 'Bill' : sb }
    return render(request, 'crm/status.html', context)

def success(request):
    f = CustomerForm(request.POST)
    return render(request, 'crm/signUp-successful.html', {'CustomerForm' : f})

def index2(request):
    #request.get['username']
    #request.post
    #l = SaleBill.objects.all()[0]
    #return HttpResponse('{0} and {1} and {2}'.format(l.saleDate, l.totalPrice, l.costumer.balance))
    return render(request, 'base.html', {})


def feedback(request) :
    f = Feedback()
    f.content = request.POST.content
    c = Customer.objects.get(username=request.user.username)
    f.Customer = c
    f.product = request.POST.productID
    f.save()
    return HttpResponse("ok")


