#from Demos.win32ts_logoff_disconnected import *
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse
from crm.forms import CustomerForm,EditForm
from wiki.models import *
from fnc.functions import *
from warehouse.models import *
from mng.forms import *

@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def index(request):
    return render(request, 'mng/base.html', {})

@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def sales(request):
    sb = SaleBill.objects.all()
    context = {'salebill': sb}
    return render(request, 'mng/mng-WikiOrder.html', context)


@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def contract_success(request):
    return render(request, 'mng/contract_success.html',{})

@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def newContract(request):
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            form.save()
            make_cb_contract(form.instance)
            return contract_success(request)

    # else:
    form = ContractForm()
    return render(request, 'mng/contract.html', {'form': form})

@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def wiki_select(request):
    wikies = Wiki.objects.all()
    context = {'wikies' : wikies}
    return render(request, 'mng/select-wiki.html', context)

@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def wiki(request , wId):
    p = Product.objects.all().filter(wiki__id = wId)
    context = {'product_list': p}
    return render(request, 'mng/mng-wiki.html', context)

@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def wrh(request):
    st = Stock.objects.all()
    context = {'stocks': st}
    return render(request, 'mng/mng-Stock.html', context)


@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def newUser(request) :
    is_delivery = Permission.objects.get(codename = 'is_deliveryman')
    is_fnc = Permission.objects.get(codename = 'is_fnc')
    is_common = Permission.objects.get( codename = 'is_common')
    is_warehouseman = Permission.objects.get( codename = 'is_warehouseman')
    is_mng_warehouse = Permission.objects.get(codename = 'is_mng_warehouse')


    if(request.POST):
        f = userForm(request.POST)
        print("ghbale is")
        if (f.is_valid()):
            print("tu iffff")
            f.instance.set_password(f.cleaned_data['password'])
            f.save()
            if (f.is_delivery) :
                f.instance.user_permissions.add(is_delivery)
            if (f.is_wrh) :
                f.instance.user_permissions.add(is_warehouseman)
            if (f.is_fnc) :
                f.instance.user_permissions.add(is_fnc)
            return contract_success(request)
    else:
        print"maaaaaaaaaan"
        f = userForm()

    return render(request , 'mng/mng-newUser.html' , {'userForm' : f})

@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def returned (request) :
    st = Stock.objects.filter(quantity_returned__gt=0)
    context = {'stocks': st}
    return render(request, 'mng/mng-Returned.html', context)
