from sales.forms import SearchForm
from wiki.models import Category, SubCat


def categories(request):
    return {'categories': Category.objects.all(), 'search_form': SearchForm()}