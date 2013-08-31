from django.utils.functional import SimpleLazyObject
from crm.models import Customer


def get_customer(request):
    try:
        return Customer.objects.get(username = request.user.username)
    except:
        return None


class NikbaadMiddleware(object):
    def process_request(self, request):
        request.customer = SimpleLazyObject(lambda: get_customer(request))