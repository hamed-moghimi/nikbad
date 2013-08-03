from django.contrib import auth
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
            #TODO: appropriate url
            return HttpResponseRedirect(reverse('sales-index'))
    return HttpResponseRedirect(reverse('sales-index'))

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('sales-index'))