from sales.models import Category, SubCat

def categories(request):
    return {'categories': Category.objects.all()}