#from Demos.win32ts_logoff_disconnected import *
from django.shortcuts import render
from django.http import HttpResponse
from crm.forms import CustomerForm,EditForm
from wiki.models import *
from crm.models import *


def index(request):
    return render(request, 'mng/base.html', {})

def sales(request):

    return render(request, 'mng/mng-sales.html', {})

def newContract(request):

    return render(request, 'mng/contract.html', {})


def wiki_select(request):
    wikies = Wiki.objects.all()
    context = {'wikies' : wikies}
    return render(request, 'mng/select-wiki.html', context)

def wiki(request , wId):
    p = Product.objects.all().filter(wiki__id = wId)
    context = {'product_list': p}
    return render(request, 'mng/mng-wiki.html', context)