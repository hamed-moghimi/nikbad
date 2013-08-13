#from Demos.win32ts_logoff_disconnected import *
from django.shortcuts import render
from django.http import HttpResponse
from crm.forms import CustomerForm,EditForm
from wiki.models import *
from warehouse.models import *
from mng.forms import ContractForm


def index(request):
    return render(request, 'mng/base.html', {})

def sales(request):
    sb = SaleBill.objects.all()
    context = {'salebill': sb}
    return render(request, 'mng/mng-WikiOrder.html', context)



def contract_success(request):
    return render(request, 'mng/contract_success.html',{})


def newContract(request):
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            form.save()
            return contract_success(request)

    # else:
    form = ContractForm()
    return render(request, 'mng/contract.html', {'form': form})


def wiki_select(request):
    wikies = Wiki.objects.all()
    context = {'wikies' : wikies}
    return render(request, 'mng/select-wiki.html', context)

def wiki(request , wId):
    p = Product.objects.all().filter(wiki__id = wId)
    context = {'product_list': p}
    return render(request, 'mng/mng-wiki.html', context)

def wrh(request):
    st = Stock.objects.all()
    context = {'stocks': st}
    return render(request, 'mng/mng-Stock.html', context)


def returned (request) :
    st = Stock.objects.filter(quantity_returned__gt=0)
    context = {'stocks': st}
    return render(request, 'mng/mng-Returned.html.html', context)
