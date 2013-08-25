# -*- encoding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models.query_utils import Q
from django.forms.models import inlineformset_factory
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from sales.forms import AdForm, AdImageForm, SearchForm, MBFrom
from sales.models import SaleBill, Ad, AdImage, MarketBasket, MarketBasket_Product, Specification
from wiki.models import Product, Wiki, Category


def baseContext(request):
    if request.customer:
        request.user = request.customer
    return {'customer': request.customer} #'wikis': Wiki.objects.all()[:20]


def index(request):
    # get new products
    new_products = Ad.objects.all()[:10]

    # get popular products
    populars = Ad.objects.all()[:10] #order_by('-popularity')[:10]
    context = baseContext(request)
    context.update({'new_products': new_products, 'populars': populars})

    if 'message' in request.GET:
        context.update({'message': request.GET['message']})
    elif 'error' in request.GET:
        context.update({'error': request.GET['error']})

    return render(request, 'sales/index.html', context)


def category(request, catID):
    catID = int(catID)
    # get new products
    new_products = Ad.objects.all().filter(product__sub_category__category__id = catID)[:10]

    # get popular products
    populars = Ad.objects.filter(product__sub_category__category__id = catID)[:10] #order_by('-popularity')[:10]
    context = baseContext(request)
    context.update({'new_products': new_products, 'populars': populars, 'category': catID,
                    'category_name': Category.objects.get(pk = catID)})
    return render(request, 'sales/index.html', context)


def detailsPage(request, itemCode):
    try:
        ad = Ad.objects.get(product__pk = itemCode)
        polls = ad.product.feedback_set.all()
    except:
        return HttpResponseRedirect(reverse('sales-index'));

    context = baseContext(request)
    context.update({'item': ad, 'polls': polls, 'now': datetime.now()})
    return render(request, 'sales/details.html', context)


MBPFormSet = inlineformset_factory(MarketBasket, MarketBasket_Product, extra = 0, form = MBFrom)


@permission_required('crm.is_customer', login_url = reverse_lazy('sales-index'))
def marketBasket(request):
    customer = request.customer
    mb = customer.marketBasket
    context = baseContext(request)

    if request.method == 'POST':
        mbForm = MBPFormSet(request.POST, instance = mb)
        if mbForm.is_valid():
            mbForm.save()
            mb.updateItems()
            context.update({'message': u'با موفقیت انجام شد'})
    else:
        mbForm = MBPFormSet(instance = mb)

    items = mb.items.all()
    for item in items:
        item.totalPrice = item.product.price * item.number

    context.update({'basket': mb, 'items': zip(items, mbForm), 'formset': mbForm})

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
ImageInlineFormSet = inlineformset_factory(Ad, AdImage, AdImageForm, extra = 1)


@permission_required('wiki.is_wiki', login_url = reverse_lazy('wiki-index'))
def adEdit(request, itemCode):
    ad = Ad.objects.get(product__pk = itemCode)

    # fixed item!
    # imageFormSet = None

    if request.POST:
        adForm = AdForm(request.POST, instance = ad)
        specFormSet = SpecInlineFormSet(request.POST, instance = ad)
        imageFormSet = ImageInlineFormSet(request.POST, request.FILES, instance = ad)
        iconForm = AdImageForm(request.POST, request.FILES, instance = ad.icon)
        if adForm.is_valid() and specFormSet.is_valid() and imageFormSet.is_valid():
            imageFormSet.save()
            adForm.instance.icon = adForm.instance.images.latest('pk') if adForm.instance.images.exists() else None
            adForm.instance.save()
            # icon = iconForm.save(commit = False)
            # icon.ad = ad
            # icon.save()

            specFormSet.save()

            # adForm.instance.icon = icon
            # adForm.instance.save()

            return HttpResponseRedirect('')
    else:
        adForm = AdForm(instance = ad)
        specFormSet = SpecInlineFormSet(instance = ad)
        imageFormSet = ImageInlineFormSet(instance = ad)
        iconForm = AdImageForm(instance = ad.icon)

    context = {'specsFormSet': specFormSet, 'imageFormSet': imageFormSet, 'ad': ad, 'adForm': adForm}
    return render(request, 'sales/adEdit.html', context)


@permission_required('crm.is_customer', raise_exception = True)
def newBuy(request):
    get = ''
    if request.GET['status'] == 'OK':
        mb = request.customer.marketBasket
        sb = SaleBill.createFromMarketBasket(mb)
        from fnc.functions import make_cb_sb

        make_cb_sb(sb)
        mb.clear()
        get = u'?message=خرید شما با موفقیت انجام شد'
    else:
        get = u'?error=خرید انجام نشد'
    return HttpResponseRedirect(reverse('sales-index') + get)


def search(request):
    # getting search query
    form = SearchForm(request.GET)
    if form.is_valid():
        cat = form.cleaned_data['category']
        query = form.cleaned_data['query']
    else:
        cat = None
        query = ''

    # retrieving matched items
    Qpname = Q(product__name__icontains = query)
    Qbname = Q(product__brand__icontains = query)
    Qwname = Q(product__wiki__companyName__icontains = query)
    itemList = Ad.objects.filter(Qbname | Qpname | Qwname)
    if cat is not None:
        itemList = itemList.filter(product__sub_category__category__name = cat)

    # PAGINATION
    paginatior = Paginator(itemList, 15)

    try:
        page = paginatior.page(request.GET['page'])
    except:
        page = paginatior.page(1)
    e = page.number
    # At last, add paginator and page to your context. See template to continue
    link = u'?category={0}&query={1}'.format(cat.pk if cat is not None else '', query)
    return render(request, 'sales/search.html',
                  {'paginator': paginatior, 'page': page, 'search_form': form, 'link': link})