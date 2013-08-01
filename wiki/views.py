from django.shortcuts import render
from django.http import HttpResponse
from wiki.models import *

def goodsList(request):
#request.get['username']
#request.post
    p = Product.objects.all()
    context = {'product_list': p}
    return render(request, 'wiki/goodslist.html', context)