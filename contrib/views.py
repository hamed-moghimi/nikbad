from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def login(request):
    print('login')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user is not None and user.is_active:
            auth.login(request, user)

            if user.has_perm('crm.is_customer'):
                # Customers
                return HttpResponseRedirect(reverse('sales-index'))
            elif user.has_perm('wiki.is_wiki'):
                # Wikis
                return HttpResponseRedirect(reverse('wiki-index'))
            elif user.has_perm('warehouse.????') or user.has_perm('warehouse.????'):
                # Warehouse admins
                return HttpResponseRedirect(reverse('warehouse-index'))
            elif user.has_perm('fnc.is_fnc'):
                # Financial admin
                return HttpResponseRedirect(reverse('fnc-index'))
            elif user.has_perm('fnc.is_manager'):
                # Manager
                return HttpResponseRedirect(reverse('mng-index'))

    return HttpResponseRedirect(reverse('index'))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))