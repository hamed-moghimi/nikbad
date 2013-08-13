from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def login(request):
    print('login')
    if request.method == 'POST':
        username    = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user is not None and user.is_active:
            auth.login(request, user)

            if user.has_perm('crm.is_customer'):
                # Customers
                return HttpResponseRedirect(reverse('sales-index'))
            elif user.has_perm('warehouse.is_warehouseman') and user.has_perm('warehouse.is_mng_warehouse'):
                # Warehouseman ke moshtarak ba manager ham dare
                return HttpResponseRedirect(reverse('warehouse-index'))
            elif user.has_perm('warehouse.is_deliveryman'):
                # Deliveryman
                return HttpResponseRedirect(reverse('warehouse-index'))
            elif user.has_perm('wiki.is_wiki'):
                # Wikis
                return HttpResponseRedirect(reverse('wiki-index'))
            elif user.has_perm('wiki.is_wiki'):
                # Warehouse admins
                return HttpResponseRedirect(reverse('wiki-index'))
            elif user.has_perm('wiki.is_wiki'):
                # Financial admin
                return HttpResponseRedirect(reverse('wiki-index'))
            elif user.has_perm('wiki.is_wiki'):
                # Manager
                return HttpResponseRedirect(reverse('wiki-index'))

    return HttpResponseRedirect(reverse('index'))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('sales-index'))