# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models.query_utils import Q
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from sales.models import SaleBill
from fnc.models import *
from fnc.forms import EmployeeForm, DateForm, AddForm, AddHesab
from datetime import timedelta, datetime


@permission_required('fnc.is_common')
def index(request):
    #request.get['username']
    #request.post
    #l = SaleBill.objects.all()[0]
    #return HttpResponse('{0} and {1} and {2}'.format(l.saleDate, l.totalPrice, l.costumer.balance))
    return render(request, 'fnc/base.html', {})


@permission_required('fnc.is_common', login_url=reverse_lazy('fnc-index'))
def gozaresh_mali(request):
#request.get['username']
#request.post
#l = SaleBill.objects.all()[0]
#return HttpResponse('{0} and {1} and {2}'.format(l.saleDate, l.totalPrice, l.costumer.balance))
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
    return render(request, 'fnc/gozaresh_mali.html', context)


@permission_required('fnc.is_manager', login_url=reverse_lazy('fnc-index'))
def sabtenam_karmand(request):
    if (request.POST):
        form = EmployeeForm(request.POST)
        if (form.is_valid()):
            form.save()
            form_test = EmployeeForm(request.POST)
            context_test = {}
            context_test.update({'emp_form': form_test})
            return render(request, 'fnc/sabtenam_karmand_review.html', context_test)
    else:
        form = EmployeeForm()
    context = {}
    context.update({'emp_form': form})
    return render(request, 'fnc/sabtenam_karmand.html', context)


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
    return render(request, 'fnc/karmandan.html', context)


@permission_required('fnc.is_common', login_url=reverse_lazy('fnc-index'))
def karmand_detail(request, epId):
    employee = Employee.objects.get(id=epId)
    rollcalls = RollCall.objects.filter(employee=epId)
    context = {}
    context.update({'rollcalls': rollcalls, 'employee': employee})
    return render(request, 'fnc/karmand_detail.html', context)


def alaki(request):
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            startDate = form.cleaned_data['startDate']
            endDate = form.cleaned_data['endDate']
            # ord = Wiki_Order.objects.filter(date__range=(startDate, endDate))

            context = {'order_list': ord}
            return render(request, 'fnc/gozares_mali.html', context)
    else:
        form = DateForm()
    return render(request, 'fnc/add_sanad.html', {'form': form})


@permission_required('fnc.is_fnc', login_url=reverse_lazy('fnc-index'))
def add_sanad(request):
    if (request.POST):
        form = AddForm(request.POST)
        if (form.is_valid()):
            form.save()
            amount = form.instance.amount
            form.instance.account_bedeh.deposit(amount)
            form.instance.account_bestan.withdraw(amount)
            context = {"sanadId": form.instance.pk}
            return render(request, 'fnc/add_sanad_2.html', context)
            #return HttpResponseRedirect(reverse('fnc-gozaresh-mali'))
    else:
        form = AddForm()
        print "form", form
    context = {}
    context.update({'add_form': form})
    return render(request, 'fnc/add_sanad.html', context)


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
    return render(request, 'fnc/karmand_edit.html', {'EditForm': f})


def daftar_kol(request):
    context = {}
    ac_ob = Account.objects.all()
    print "salam", ac_ob.count()
    context.update({'accounts': ac_ob})
    return render(request, 'fnc/daftar_kol.html', context)


def daftar_kol_2(request, daftarId):
    context = {}
    account = Account.objects.get(id=daftarId)
    q1 = Q(account_bedeh=account)
    q2 = Q(account_bestan=account)
    rows = CostBenefit.objects.filter(q1 | q2).order_by("-date")
    context.update({"account": account})
    context.update({'name': account.name})
    context.update({'costBenefits': rows})

    sum_bedeh = 0
    sum_bestan = 0

    cb_bedeh = CostBenefit.objects.filter(account_bedeh=account)
    for cb in cb_bedeh:
        sum_bedeh += cb.amount
    context.update({"sum_bedeh": sum_bedeh})

    cb_bestan = CostBenefit.objects.filter(account_bestan=account)
    for cb in cb_bestan:
        sum_bestan += cb.amount
    context.update({"sum_bestan": sum_bestan})

    return render(request, 'fnc/daftar_kol_2.html', context)


def taraz_azmayeshi(request):
    context = {}
    tarazes = Taraz.objects.all()
    context.update({"tarazes": tarazes})
    return render(request, 'fnc/taraz_azmayeshi.html', context)


def taraz_azmayeshi_2(request, tarazId):
    context = {}
    tz_ob = Taraz.objects.get(id=tarazId)
    sum_g_bedeh=0
    sum_g_bestan=0
    sum_m_bedeh=0
    sum_m_bestan=0

    context.update({"tarazes": tz_ob})


    for x in tz_ob.rows_taraz.all():
        sum_g_bedeh+=x.gardesh_bedeh
        sum_g_bestan+=x.gardesh_bestan
        sum_m_bedeh+=x.mande_bedeh
        sum_m_bestan+=x.mande_bestan
    context.update({'s1': sum_g_bedeh, 's2': sum_g_bestan, 's3': sum_m_bedeh, 's4': sum_m_bestan})
    return render(request, 'fnc/taraz_azmayeshi_2.html', context)


def add_hesab(request):
    if (request.POST):
        form = AddHesab(request.POST)
        if (form.is_valid()):
            form.save()
            print "nameeeee", form.instance.name
            print "salam", form.instance.amount
            context=({'name': form.instance.name}, {'amount': form.instance.amount})
            print context, "hhhhhhhhh"
            return render(request, 'fnc/add_hesab_2.html', context)
            #return HttpResponseRedirect(reverse('fnc-gozaresh-mali'))
    else:
        form = AddHesab()
        print "form", form
    context = {}
    context.update({'hazine_form': form})


    return render(request, 'fnc/add_hesab.html', context)

def resid_emp(request):
    context={}
    sf_ob= SalaryFactor.objects.all()
    context.update({"salaryFac": sf_ob})
    return render(request, 'fnc/resid_emp.html', context)