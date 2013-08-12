#from Demos.win32ts_logoff_disconnected import *
from django.shortcuts import render
from django.http import HttpResponse
from crm.forms import CustomerForm,EditForm
from datetime import *
from crm.models import *
from sales.models import *
from fnc.models import *
from wiki.models import *

def base(request):

    return render(request, 'mng/base.html', {})


def emp_detail(request , epId):
    employee=Employee.objects.get(id=epId)
    rollcalls=RollCall.objects.filter(employee=epId)
    context = {}
    context.update({'rollcalls': rollcalls, 'employee': employee })
    return render(request, 'mng/mng-emp-detail.html', context)

def emp(request):
    employees = Employee.objects.all()
    for ep in employees:
        rollcalls= RollCall.objects.filter(employee=ep)
        ep.hours=timedelta()
        for rc in rollcalls:
            enter= datetime.combine(rc.date,rc.entrance_time)
            exit = datetime.combine(rc.date,rc.exit_time)
            ep.hours+=enter-exit
    context = {}
    context.update({'employees': employees})
    return render(request, 'mng/mng-emp.html', context)

def wrh(request):

    return render(request, 'mng/mng-wrh.html', {})


def fnc(request):
    cb_objects = CostBenefit.objects.all()
    context = {}
    context.update({'costBenefits': cb_objects})
    sb_objects = SaleBill.objects.all()
    context.update({'saleBills': sb_objects})
    return render(request, 'mng/mng-fnc.html', context)

def sales(request):

    return render(request, 'mng/mng-sales.html', {})

def select_wiki(request):
    wikies = Wiki.objects.all()
    context = {'wikies':wikies}
    return render(request, 'mng/select-wiki.html', context)

def wiki(request , wId):
    # if request.user.is_authenticated():
    #     user = request.user
    #     myName = user.username
    p = Product.objects.all().filter( wiki__id = wId)
    context = {'product_list': p}
    return render(request, 'mng/mng-wiki.html', context)
