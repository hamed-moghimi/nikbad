from django.shortcuts import render
from django.http import HttpResponse
from sales.models import SaleBill


def index(request):
    request.get['username']
    request.post
    l = SaleBill.objects.all()[0]
    return HttpResponse('{0} and {1} and {2}'.format(l.saleDate, l.totalPrice, l.costumer.balance))