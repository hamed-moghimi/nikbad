# -*- encoding: utf-8 -*-
from django.shortcuts import render

def index(request):
    a = u'سامانه انار'
    context = {'name': a}
    return render(request, 'wrh/index.html', context)