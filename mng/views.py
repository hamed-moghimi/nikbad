# -*- encoding:utf-8 -*-
#from Demos.win32ts_logoff_disconnected import *
from audioop import reverse
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from reportlab.lib.pagesizes import letter, landscape
from contrib.email import render_and_email
from contrib.pdf import StringMark, getPDF_Response
from wiki.models import *
from warehouse.models import *
from mng.forms import *
from fnc.models import *
from fnc.forms import *
from datetime import *


@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def index(request):
    return render(request, 'mng/base.html', {})


@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def gozaresh_mali(request):
#request.get['username']
#request.post
#l = SaleBill.objects.all()[0]
#return HttpResponse('{0} and {1} and {2}'.format(l.saleDate, l.totalPrice, l.costumer.balance))
    print "heeeeeeeeeeeeeeeellllllllllllllllllllllllllllll"
    cb_objects = []
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            startDate = form.cleaned_data['startDate']
            endDate = form.cleaned_data['endDate']
            cb_objects = CostBenefit.objects.filter(date__range=(startDate, endDate))

    else:
        form = DateForm()
        cb_objects = CostBenefit.objects.all()
    paginator = Paginator(cb_objects, 25)
    page = request.GET.get('page')
    try:
        cb_ob = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        cb_ob = paginator.page(1)
    except EmptyPage:
        cb_ob = paginator.page(paginator.num_pages)

    context = {}
    context.update({'costBenefits': cb_ob, 'form': form})
    return render(request, 'mng/gozaresh_mali.html', context)


@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def newUser(request):
    is_delivery = Permission.objects.get(codename='is_deliveryman')
    is_fnc = Permission.objects.get(codename='is_fnc')
    is_common = Permission.objects.get(codename='is_common')
    is_warehouseman = Permission.objects.get(codename='is_warehouseman')
    is_mng_warehouse = Permission.objects.get(codename='is_mng_warehouse')

    if (request.POST):
        f = userForm(request.POST)
        print("ghbale is")
        if (f.is_valid()):
            print("tu iffff")
            f.instance.set_password(f.cleaned_data['password'])
            f.instance.first_name = f.instance.first_name + " " + f.instance.last_name
            f.instance.last_name = f.cleaned_data['ssn']
            print f.instance.last_name
            f.save()

            if (f.cleaned_data['is_delivery']):
                f.instance.user_permissions.add(is_delivery)
            if (f.cleaned_data['is_wrh']):
                f.instance.user_permissions.add(is_warehouseman, is_mng_warehouse)
            if (f.cleaned_data['is_fnc']):
                f.instance.user_permissions.add(is_fnc, is_common)
            context={'first_name':f.cleaned_data['first_name'] , 'last_name':f.cleaned_data['last_name'],
                     'username':f.cleaned_data['username'],'password':f.cleaned_data['password']}
            render_and_email([f.cleaned_data['email']], u'ثبت کاربر جدید', u"عضو شدید", 'mng/signUp_email.html',context)
            return success(request)

    else:

        print"maaaaaaaaaan"
        f = userForm()

    return render(request, 'mng/mng-newUser.html', {'userForm': f})




@permission_required('fnc.is_common', login_url=reverse_lazy('fnc-index'))
def karmand_detail(request, epId):
    employee = Employee.objects.get(id=epId)
    rollcalls = RollCall.objects.filter(employee=epId)
    context = {}
    context.update({'rollcalls': rollcalls, 'employee': employee})
    return render(request, 'mng/karmand_detail.html', context)


def karmand_detail_2(request, epId):
    employee = Employee.objects.get(id=epId)
    f = EmployeeForm(instance=employee)
    if (request.POST):
        f = EmployeeForm(request.POST, instance=employee)
        try:
            request.POST['gender'] = request.POST['gender'].encode('utf-8')
        except:
            pass
        if (f.is_valid()):
            f.save()
            return HttpResponseRedirect(reverse('fnc-karmandan'))
        # else :
    return render(request, 'mng/karmand_edit.html', {'EditForm': f})


@permission_required('fnc.is_manager', login_url=reverse_lazy('fnc-index'))
def sabtenam_karmand(request):
    if (request.POST):
        form = EmployeeForm(request.POST)
        if (form.is_valid()):
            form.save()
            form_test = EmployeeForm(request.POST)
            context_test = {}
            context_test.update({'emp_form': form_test})
            return render(request, 'mng/sabtenam_karmand_review.html', context_test)
    else:
        form = EmployeeForm()
    context = {}
    context.update({'emp_form': form})
    return render(request, 'mng/sabtenam_karmand.html', context)

@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def returned(request):
    st = Stock.objects.filter(quantity_returned__gt=0)
    context = {'stocks': st}
    return render(request, 'mng/mng-Returned.html', context)


@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def contractDetail(request, wId):
    c = Contract.objects.get(wiki__id=wId)
    name = Wiki.objects.get(id=wId)
    print c.id
    print wId
    f = ContractEdit(instance=c)

    context = {'ContractEdit': f, 'c': c, 'wiki': wId, 'name': name}
    return render(request, 'mng/contract-detail.html', context)


@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def contractEdit(request, wId):
    c = Contract.objects.get(wiki__id=wId)
    name = Wiki.objects.get(id=wId)
    if (request.POST):
        f = ContractEdit(request.POST, instance=c)
        if (f.is_valid()):
            f.save()
            return contract_success(request, wId)
    f = ContractEdit(instance=c)
    context = {'ContractEdit': f, 'c': c, 'wiki': wId, 'name': name}
    return render(request, 'mng/contract-edit.html', context)


@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def sales(request):
    sb = []

    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            startDate = form.cleaned_data['startDate']
            endDate = form.cleaned_data['endDate']
            sb = SaleBill.objects.all().filter(date__range=(startDate, endDate))
    else:
        form = DateForm()
    context = {}
    context.update({'salebill': sb, 'form': form})
    return render(request, 'mng/mng-sales.html', context)


@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def conReq(request):
    data = ConRequest.objects.all().order_by('-pub_date')
    context = {'data': data}
    return render(request, 'mng/mng-con-req.html', context)

@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def saleDetail(request, wId):
    sb = SaleBill.objects.get(id=wId)
    p = sb.products.all()
    context = {'product': p, 'saleBill': sb}
    return render(request, 'mng/sale-detail.html', context)


@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def contract_success(request, wId):
    a = []
    a = ConRequest.objects.filter(wiki__id=wId)
    print a.count
    if ( a.count() != 0):
        print "maaaaaaaaaaaaaaan"
        ConRequest.objects.get(wiki__id=wId).delete()
        return render(request, 'mng/contract_success.html', {})
    else:
        print "elseeeeeeeeee"
        return render(request, 'mng/contract_success.html', {})

@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def success(request):
    return render(request, 'mng/contract_success.html', {})


@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def newContract(request, wId):
    w = Wiki.objects.get(pk=wId)
    print w.id
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            form.instance.wiki = w
            form.instance.companyName = w.companyName
            form.instance.fee = ConRequest.objects.get(wiki=w).abonne
            # form.instance.fee = ConRequest.objects.get(wiki=w).
            form.instance.percent = ConRequest.objects.get(wiki=w).benefit
            form.save()
            # make_cb_contract(form.instance)
            return contract_success(request, wId)
    else:
        form = ContractForm(initial={'wiki': w, 'companyName': w.companyName,
                                     'fee': ConRequest.objects.get(wiki=Wiki.objects.get(pk=wId)).abonne,
                                     'percent': ConRequest.objects.get(wiki=w).benefit})

    return render(request, 'mng/contract.html', {'form': form})


@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def wiki_select(request):
    wikies = Wiki.objects.all()

    cont = Contract.objects.all()
    context = {'wikies': wikies, 'conts': cont}
    return render(request, 'mng/select-wiki.html', context)


@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def wiki(request, wId):
    p = Product.objects.all().filter(wiki__id=wId)
    w = Wiki.objects.get(id=wId)
    context = {'product_list': p, 'wiki': w}
    return render(request, 'mng/mng-wiki.html', context)


@permission_required('fnc.is_common', login_url=reverse_lazy('fnc-index'))
def karmandan(request):
    employees = Employee.objects.all()
    for ep in employees:
        rollcalls = RollCall.objects.filter(employee=ep)
        ep.hours = timedelta()
        for rc in rollcalls:
            enter = datetime.combine(rc.date, rc.entrance_time)
            exit = datetime.combine(rc.date, rc.exit_time)
            ep.hours += exit - enter
    context = {}
    context.update({'employees': employees})
    return render(request, 'mng/karmandan.html', context)


@permission_required('fnc.is_manager', login_url=reverse_lazy('index'))
def wrh(request):
    st = Stock.objects.all()
    first_msg = "کالاهای موجود در انبار به شرح زیر می باشند:"
    # prt = reverse('WRH_Print_Stock')
    st = Stock.objects.filter(quantity__gt=0).order_by('product__goodsID')
    if not st:
        first_msg = "انبار خالی است."
    paginator = Paginator(st, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except Exception as s:
        print(str(s))
        contacts = paginator.page(1)

    context = {'stocks': contacts, 'first_msg': first_msg, 'paginator': paginator,
               'contacts': contacts}
               # 'print': prt}
    return render(request, 'mng/mng-Stock.html', context)


