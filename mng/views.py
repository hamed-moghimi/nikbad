# -*- encoding:utf-8 -*-
#from Demos.win32ts_logoff_disconnected import *
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse
from contrib.email import render_and_email
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
    return render(request, 'mng/mng-sales.html', context)

@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def conReq(request):
    data=ConRequest.objects.all().order_by('-pub_date')
    context = {'data': data}
    return render(request, 'mng/mng-con-req.html', context)

# @permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
# def conReq(request):
#     data=ConRequest.objects.all().order_by('-pub_date')
#     context = {'data': data}
#     return render(request, 'mng/mng-con-req.html', context)

@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def saleDetail(request ,wId):
    sb = SaleBill.objects.get(id=wId)
    p = sb.products.all()
    context = {'product' : p , 'saleBill' : sb}
    return render(request,'mng/sale-detail.html' , context)

@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def contract_success(request , wId):
    a=[]
    a= ConRequest.objects.filter(wiki__id=wId)
    print a.count
    if( a.count()!=0):
        print "maaaaaaaaaaaaaaan"
        ConRequest.objects.get(wiki__id=wId).delete()
        return render(request, 'mng/contract_success.html',{})
    else:
        print "elseeeeeeeeee"
        return render(request, 'mng/contract_success.html',{})

@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def newContract(request ,wId):
    w = Wiki.objects.get(pk=wId)
    print w.id
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            form.instance.wiki = w
            form.instance.companyName =w.companyName
            form.instance.fee=ConRequest.objects.get(wiki=w).abone
            form.instance.percent= ConRequest.objects.get(wiki=w).benefit
            form.save()
            # make_cb_contract(form.instance)
            return contract_success(request ,wId)
    else:
        form = ContractForm(initial={'wiki': w,'companyName':w.companyName ,'fee':ConRequest.objects.get(wiki=Wiki.objects.get(pk=wId)).abone ,'percent':ConRequest.objects.get(wiki=w).benefit})

    return render(request, 'mng/contract.html', {'form': form})

@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def wiki_select(request):
    wikies = Wiki.objects.all()
    cont = Contract.objects.all()
    context = {'wikies' : wikies , 'conts':cont}
    return render(request, 'mng/select-wiki.html', context)

@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def wiki(request , wId):
    p = Product.objects.all().filter(wiki__id = wId)
    w = Wiki.objects.get(id=wId)
    context = {'product_list': p , 'wiki' : w}
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
            f.instance.first_name = f.instance.first_name+" "+f.instance.last_name
            f.instance.last_name = f.cleaned_data['ssn']
            print f.instance.last_name
            context={'first_name':f.cleaned_data['first_name'] , 'last_name':f.cleaned_data['last_name']}
            render_and_email([f.cleaned_data['email']], u'ثبت کاربر جدید', u"عضو شدید", 'crm/signUp_email.html',context)
            f.save()

            if (f.cleaned_data['is_delivery']) :
                f.instance.user_permissions.add(is_delivery)
            if (f.cleaned_data['is_wrh']) :
                f.instance.user_permissions.add(is_warehouseman , is_mng_warehouse)
            if (f.cleaned_data['is_fnc']) :
                f.instance.user_permissions.add(is_fnc , is_common)
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


@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def contractDetail(request ,wId):
    c = Contract.objects.get(wiki__id=wId)
    name=Wiki.objects.get(id=wId)
    print c.id
    print wId
    f = ContractEdit( instance=c )

    context = {'ContractEdit' :f ,'c':c , 'wiki' : wId ,'name':name}
    return render(request, 'mng/contract-detail.html', context)

@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def contractEdit(request ,wId):
    c = Contract.objects.get(wiki__id=wId)
    name=Wiki.objects.get(id=wId)
    if(request.POST):
        f = ContractEdit(  request.POST  , instance=c)
        if (f.is_valid()):
            f.save()
            return contract_success(request,wId)
    f = ContractEdit( instance=c )
    context = {'ContractEdit' :f ,'c':c , 'wiki' : wId , 'name':name}
    return render(request, 'mng/contract-edit.html', context)

