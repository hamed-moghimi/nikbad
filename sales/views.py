# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.models import inlineformset_factory
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.utils import timezone
from sales.forms import SaleBillForm, AdForm
from sales.models import SaleBill, Ad, AdImage, MarketBasket, MarketBasket_Product, Specification
from crm.models import Customer, Feedback
from wiki.models import Product, Wiki, Category, SubCat


# gets all wikis to display in menu bar
from wiki.views import goodsList


def baseContext(request):
    if request.customer:
        request.user = request.customer
    return {'wikis': Wiki.objects.all()[:20], 'customer': request.customer}


def index(request):
    # get new products
    new_products = Ad.objects.all()[:10]

    # get popular products
    populars = Ad.objects.all()[:10] #order_by('-popularity')[:10]
    context = baseContext(request)
    context.update({'new_products': new_products, 'populars': populars})
    print context
    return render(request, 'sales/index.html', context)


def category(request, catID):
    catID = int(catID)
    # get new products
    new_products = Ad.objects.all().filter(product__sub_category__category__id = catID)[:10]

    # get popular products
    populars = Ad.objects.filter(product__sub_category__category__id = catID)[:10] #order_by('-popularity')[:10]
    context = baseContext(request)
    context.update({'new_products': new_products, 'populars': populars, 'category': catID})
    return render(request, 'sales/index.html', context)


def detailsPage(request, itemCode):
    try:
        ad = Ad.objects.get(id = itemCode)
        polls = ad.product.feedback_set.all()
    except:
        return HttpResponseRedirect(reverse('sales-index'));

    context = baseContext(request)
    context.update({'item': ad, 'polls': polls})
    return render(request, 'sales/details.html', context)


@permission_required('crm.is_customer', login_url = reverse_lazy('sales-index'))
def marketBasket(request):
    #TODO: market basket form
    customer = request.customer
    # temporary codes
    if request.method == 'POST':
        SaleBill.createFromMarketBasket(customer.marketBasket)
        customer.marketBasket.clear()
        return render(request, 'sales/success.html', {})

    items = customer.marketBasket.items.all()
    for item in items:
        item.totalPrice = item.product.price * item.number

    context = baseContext(request)
    context.update({'basket': customer.marketBasket, 'items': items})
    return render(request, 'sales/basket.html', context)


@permission_required('crm.is_customer', raise_exception = True)
def addToMarketBasket(request, pId):
    if request.is_ajax():
        mb = request.customer.marketBasket
        p = Product.objects.get(pk = pId)
        mb.add_item(p)
        return HttpResponse(mb.itemsNum)
        # return HttpResponseForbidden()


SpecInlineFormSet = inlineformset_factory(Ad, Specification, extra = 1)
ImageInlineFormSet = inlineformset_factory(Ad, AdImage, extra = 1)

#@permission_required('wiki.is_wiki', login_url = reverse_lazy('wiki-index'))
def adEdit(request, itemCode):
    ad = Ad.objects.get(product__pk = itemCode)

    adForm = AdForm(instance = ad)
    specFormSet = SpecInlineFormSet(instance = ad)
    imageFormSet = ImageInlineFormSet(instance = ad)

    context = {'specsFormSet': specFormSet, 'imageFormSet': imageFormSet, 'ad': ad, 'adForm': adForm}
    return render(request, 'sales/adEdit.html', context)
