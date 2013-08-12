#from Demos.win32ts_logoff_disconnected import *
from django.shortcuts import render
from django.http import HttpResponse
from crm.forms import CustomerForm,EditForm

from crm.models import *


def base(request):

    return render(request, 'mng/base.html', {})

def emp(request):

    return render(request, 'mng/mng-emp.html', {})

def wrh(request):

    return render(request, 'mng/mng-wrh.html', {})


def fnc(request):

    return render(request, 'mng/mng-fnc.html', {})

def sales(request):

    return render(request, 'mng/mng-sales.html', {})

def wiki(request):

    return render(request, 'mng/mng-wiki.html', {})
