from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from sales.models import SaleBill
from fnc.models import *
from fnc.forms import EmployeeForm, DateForm, AddForm
from datetime import timedelta, datetime


@permission_required('fnc.is_common')
def index(request):
    #request.get['username']
    #request.post
    #l = SaleBill.objects.all()[0]
    #return HttpResponse('{0} and {1} and {2}'.format(l.saleDate, l.totalPrice, l.costumer.balance))
    return render(request, 'fnc/base.html', {})


@permission_required('fnc.is_common', login_url = reverse_lazy('fnc-index'))
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
            cb_objects = CostBenefit.objects.filter(date__range = (startDate, endDate))

    else:
        form = DateForm()
        cb_objects = CostBenefit.objects.all()

    context = {}
    context.update({'costBenefits': cb_objects, 'form': form})
    return render(request, 'fnc/gozaresh_mali.html', context)


@permission_required('fnc.is_manager', login_url = reverse_lazy('fnc-index'))
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


@permission_required('fnc.is_common', login_url = reverse_lazy('fnc-index'))
def karmandan(request):
    employees = Employee.objects.all()
    for ep in employees:
        rollcalls = RollCall.objects.filter(employee = ep)
        ep.hours = timedelta()
        for rc in rollcalls:
            enter = datetime.combine(rc.date, rc.entrance_time)
            exit = datetime.combine(rc.date, rc.exit_time)
            ep.hours += exit - enter
    context = {}
    context.update({'employees': employees})
    return render(request, 'fnc/karmandan.html', context)


@permission_required('fnc.is_common', login_url = reverse_lazy('fnc-index'))
def karmand_detail(request, epId):
    employee = Employee.objects.get(id = epId)
    rollcalls = RollCall.objects.filter(employee = epId)
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


@permission_required('fnc.is_fnc', login_url = reverse_lazy('fnc-index'))
def add_sanad(request):
    if (request.POST):
        form = AddForm(request.POST)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect(reverse('fnc-gozaresh-mali'))
    else:
        form = AddForm()
        print "form", form
    context = {}
    context.update({'add_form': form})
    return render(request, 'fnc/add_sanad.html', context)


def karmand_detail_2(request, epId):
    employee = Employee.objects.get(id = epId)
    f = EmployeeForm(instance = employee)
    if (request.POST):
        f = EmployeeForm(request.POST, instance = employee)
        try:
            request.POST['gender'] = request.POST['gender'].encode('utf-8')
        except:
            pass
        if (f.is_valid()):
            f.save()
            return HttpResponseRedirect(reverse('fnc-karmandan'))
    # else :
    return render(request, 'fnc/karmand_edit.html', {'EditForm': f})