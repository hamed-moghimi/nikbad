from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None and user.is_active():
            login(request, user)
            #TODO: appropriate url
            return HttpResponseRedirect('sales-index')