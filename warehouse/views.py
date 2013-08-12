# -*- encoding: utf-8 -*-
from operator import pos
from django.shortcuts import render
from sales.models import *
from wiki.models import *
from warehouse.models import *

def index(request):
    a = u'سامانه انار'
    context = {'name': a}
    return render(request, 'wrh/base.html', context)

#***********************************************************************************************************
#***********************************BEGIN NEW ORDERS*******************************************************
def new_order(request):
    bill = SaleBill.objects.filter(deliveryStatus = 0)
    transference = Transference.objects.all()
    wiki_return = ReturnRequest.objects.filter(deliveryStatus = 0)
    for b in bill:
        clear = Clearance.objects.filter(bill=b)
        if clear.all():
           print("ghablan sabt shode")
        else:
            cl = Clearance(type='sale', date=b.saleDate, bill=b)
            cl.save()
    for tr in transference:
        clear = Clearance.objects.filter(transfer=tr)
        if clear.all():
            print("ghablan sabt shode")
        else:
            cl = Clearance(type='warehouse', date=tr.date, transfer=tr)
            cl.save()
    for w in wiki_return:
        clear = Clearance.objects.filter(wiki=w)
        if clear.all():
            print("ghablan sabt shode")
        else:
            cl = Clearance(type='wiki', date=w.pub_date, wiki=w)
            cl.save()

    clrs=Clearance.objects.filter(ready='n').order_by('date')
    context = {'clrs': clrs, 'active_menu': 2}
    return render(request, 'wrh/NewOrders.html', context)

def new_order_back(request):
    bill = SaleBill.objects.filter(deliveryStatus = 0)
    transference = Transference.objects.all()
    wiki_return = ReturnRequest.objects.all()
    for b in bill:
        clear = Clearance.objects.filter(bill=b)
        if clear.all():
            print("ghablan sabt shode")
        else:
            cl = Clearance(type='sale', date=b.saleDate, bill=b)
            cl.save()
    for tr in transference:
        clear = Clearance.objects.filter(transfer=tr)
        if clear.all():
            print("ghablan sabt shode")
        else:
            cl = Clearance(type='warehouse', date=tr.date, transfer=tr)
            cl.save()
    for w in wiki_return:
        clear = Clearance.objects.filter(wiki=w)
        if clear.all():
            print("ghablan sabt shode")
        else:
            cl = Clearance(type='wiki', date=w.pub_date, wiki=w)
            cl.save()

    clrs=Clearance.objects.filter(ready='n').order_by('date')
    context = {'clrs': clrs, 'active_menu': 2}
    return render(request, 'wrh/NewOrdersBack.html', context)

def tiny_order(request, pid):
    p2 = int(pid)
    a = Clearance.objects.get(pk=p2)
    context = {'clrs': a}
    return render(request, 'wrh/Tiny_Order.html', context)

def confirm_order(request, pid):
    context = {}
    p = int(pid)
    clr = Clearance.objects.get(pk=p)
    check = False
    # va3 havalehaayi ke maale samaneye forushe xodesh reserve mikone o nabudesho check mikone vali va3 ersaale mojadade mayoub haa emkan dare kalaa kam biad
    if clr.type=='warehouse':
        p = clr.transfer.product.pk
        pr = Product.objects.get(pk=p)
        st = Stock.objects.filter(product=pr)
        if st.all():
            if (st[0].quantity-st[0].reserved_quantity)<clr.transfer.quantity:
                check_order_point(p)
                check = True
        else:
            check_order_point(p)
            check = True

    if check:
        context = {'error': "این حواله به علت کمبود موجودی انبار آماده تحویل نیست :("}
    else:
        clr.ready = 'r'
        clr.save()
        if clr.type=='warehouse':
            p = clr.transfer.product.pk
            pr = Product.objects.get(pk=p)
            st = Stock.objects.get(product=pr)
            st.reserved_quantity += clr.transfer.quantity
            st.save()
            check_order_point(p)
        context = {'msg': "کالاهای موجود در حواله انتخاب شده، آماده خروج از انبار هستند:)"}
    return render(request, 'wrh/ConfirmOrder.html', context)
#****************************************END NEW ORDER*****************************************
#**********************************************************************************************


#***********************************************************************************************************
#***********************************BEGIN NEW READY ORDERS**************************************************
def ready_order(request):
    clrs = Clearance.objects.filter(ready='r').order_by('date')
    context = {'clrs': clrs}
    return render(request, 'wrh/ReadyOrder.html', context)

def ready_order_back(request):
    print ("tu readye order back")
    clrs = Clearance.objects.filter(ready='r').order_by('date')
    context = {'clrs': clrs}
    return render(request, 'wrh/ReadyOrder2.html', context)

def ready_tiny_order (request, pid):
    print ("tu ready tiny order")
    print(pid)
    p2 = int(pid)
    a = Clearance.objects.get(pk=p2)
    context = {'clrs': a}
    return render(request, 'wrh/ReadyTiny_Order.html', context)

def confirm_ready_order(request, pid):
    context = {}
    p = int(pid)
    clr = Clearance.objects.get(pk=p)
    # reside xoruj az anbaar saader mishe
    rc = Receipt_Clearance(clearance=clr)
    rc.save()
    #havale be halate out dar miad
    clr.ready = 'o'
    clr.save()
    # hame be halate dar raah tabdil shavand
    if clr.type=='sale':
        bl = clr.bill
        bl.deliveryStatus = 1
        bl.save()
    else:
        if clr.type=='wiki':
            wk = clr.wiki
            wk.deliveryStatus = 1
            wk.save()
    # az mowjudi va reservi haaye anbaar kam she
    if clr.type=='sale':
        for pro in clr.bill.products.all():
            p2 = pro.product.pk
            pr = Product.objects.get(pk=p2)
            st = Stock.objects.get(product=pr)
            st.quantity -= pro.number
            st.reserved_quantity -= pro.number
            st.save()
            check_order_point(p2)
    else:
        if clr.type=='warehouse':
            p = clr.transfer.product.pk
            pr = Product.objects.get(pk=p)
            st = Stock.objects.get(product=pr)
            st.quantity -= clr.transfer.quantity
            st.reserved_quantity -= clr.transfer.quantity
            st.save()
            check_order_point(p)
        else:
            p = clr.wiki.product.pk
            pr = Product.objects.get(pk=p)
            st = Stock.objects.get(product=pr)
            if clr.wiki.returned_only:
                st.quantity_returned = 0
                st.save()
            else:
                st.quantity = 0
                st.quantity_returned = 0
                st.reserved_quantity = 0
                st.save()
    context = {'msg': "این حواله با موفقیت از انبار خارج شد و سند خروج از انبار ثبت گردید :)"}
    return render(request, 'wrh/ConfirmReadyOrder.html', context)
#****************************************END NEW READY ORDER***********************************
#**********************************************************************************************


#***********************************************************************************************************
#***********************************BEGIN WAREHOUSE DELIVERY*******************************************************
def delivery_wiki_select(request):
    a = Wiki.objects.all()
    context = {'wikis': a, 'active_menu': 1}
    return render(request,'wrh/WRHDelivery.html', context)

def delivery_wiki_select2(request):
    a = Wiki.objects.all()
    context = {'wikis': a}
    return render(request,'wrh/WRHDelivery2.html', context)


def delivery_product_select(request, pid):
    wik = Wiki.objects.filter(pk=pid)
    a = Product.objects.filter(wiki=wik)
    context = {'products': a}
    return render(request,'wrh/WRHDelivery-next.html', context)

def confirm_wrh_delivery(request):
    context = {}
    if request.method == 'POST':
        try:
            post = request.POST
            if check_capacity():
                for key, value in post.iteritems():
                    if key[:4]=="qnt_":
                        num = int(key[4:])
                        prd = Product.objects.get(pk=num)
                        stck = Stock.objects.filter(product=prd)
                        wk = prd.wiki
                        vl = int(value)
                        if vl:
                            if not stck:
                                st = Stock(product=prd , quantity= value, quantity_returned=0, rack_num_returned=0, rack_num=0 )
                                st.save()
                                print(st.quantity)
                            else:
                                stck[0].quantity += int(value)
                                stck[0].save()
                            receipt_del = Receipt_Delivery(wiki=wk, product=prd, quantity=vl)
                            receipt_del.save()
                    else:
                        if key[:7]=="volume_":
                            num = int(key[7:])
                            prd = Product.objects.get(pk=num)
                            prd.volume = int(value)
                            prd.save()
            else:
                context = {'error': "ظرفیت انبار برای ورود کالاهای زیر کافی نیست :("}
        except Exception as e:
            print(str(e))
    return render(request,'wrh/ConfirmationWRHDelivery.html', context)
#****************************************END WAREHOUSE DELIVERY***********************************
#**********************************************************************************************


#***********************************************************************************************************
#***********************************BEGIN CUSTOMER RETURN*******************************************************
def customer_return(request):
    context = { 'active_menu': 3}
    return render(request, 'wrh/CustomerReturn.html', context)

def customer_return2(request):
    context = { 'active_menu': 3}
    return render(request, 'wrh/CustomerReturn2.html', context)

def customer_return_next(request, pid , kid):
    context = {}
    p2 = int(pid)
    k2 = int(kid)
    try:
        clr = Clearance.objects.get(pk=p2)
        if clr.ready!='o':
            context = {'error':"کالاهای این حواله هنوز از انبار خارج نشده است."}
        else:
            try:
                pr = Product.objects.get(goodsID=k2)
                if clr.type=='sale':
                    if clr.bill.deliveryStatus==2:
                        context = {'error': "رسید کالاهای مربوط به این حواله قبلا در سیستم به ثبت رسیده است."}
                    else:
                        pro2 = clr.bill.products.all().get(product=pr)
                        pro3 = pro2.product
                        tr = Transference.objects.filter(bill=(clr.bill), product=pr)
                        if tr.all():
                            context = {'error': "تعداد کالای معیوب از این نوع برای حواله انتخاب شده قبلا در سیستم به ثبت رسیده است."}
                        else:
                            context = {'clr': clr, 'product': pro3}
                else:
                    if clr.type=='warehouse':
                        if clr.transfer.bill.deliveryStatus==2:
                            context = {'error': "رسید کالاهای مربوط به این حواله قبلا در سیستم به ثبت رسیده است."}
                        else:
                            if clr.transfer.product.pk!=pr.pk:
                                context = {'error': "کالایی با شماره داده شده در این حواله یافت نشد."}
                            else:
                                pro3 = clr.transfer.product
                            tr = Transference.objects.filter(bill=(clr.transfer.bill), product=pr, defective='d')
                            if tr.all():
                                context = {'error': "تعداد کالای معیوب از این نوع برای حواله انتخاب شده قبلا در سیستم به ثبت رسیده است."}
                            else:
                                context = {'clr': clr, 'product': pro3}
                    else:
                        context = {'error': "کالای معیوب از ویکی دربافت نمی شود."}
            except Exception as e:
                print(str(e))
                context = {'error': "کالایی با شماره داده شده در این حواله یافت نشد."}
    except Exception as e:
        context = {'error': "حواله ای با شماره داده شده یافت نشد."}

    return render(request, 'wrh/CustomerReturn-next.html', context)

def confirm_return(request, pid, kid, cid):
    context = {}
    clr_id = int(pid)
    pro_id = int(kid)
    qnt = int(cid)
    clr = Clearance.objects.get(pk=clr_id)
    pr = Product.objects.get(goodsID=pro_id)
    if clr.type=='sale':
        pro = clr.bill.products.all().get(product=pr)
        quan = pro.number
        p2 = pro.product
    else:
        if clr.type=='warehouse':
            quan = clr.transfer.quantity
            p2 = clr.transfer.product
    if quan<qnt:
        context={'error': "مقدار وارد شده برای کالای مرجوعی بیش تر از مقدار ثبت شده در حواله است.", 'pid':pid, 'kid':kid}
    else:
        try:
            stck= Stock.objects.get(product=p2)
            stck.quantity_returned += qnt
            if clr.type=='sale':
                tr = Transference(bill=(clr.bill), product=p2, quantity=qnt)
                tr.save()
            else:
                if clr.type=='warehouse':
                    t = clr.transfer
                    t.defective = 'd'
                    t.save()
                    tr = Transference(bill=(clr.transfer.bill), product=p2, quantity=qnt)
                    tr.save()
            check_order_point(p2.pk)
            context = {'msg': "کالاهای معیوب با موفقیت در لیست کالاهای مرجوعی ثبت شده و حواله جدید برای ارسال مجدد کالا صادر گردید."}
            stck.save()
        except Exception as e:
            print(str(e))
    return render(request, 'wrh/ConfirmReturn.html', context)
#****************************************END CUSTOMER RETURN***********************************
#**********************************************************************************************

#***********************************************************************************************************
#***********************************BEGIN CUSTOMER WIKI RECEIPT*******************************************************
def ReceiptDelivery(request):
    context = {}
    return render(request,'wrh/ReceiptDelivery.html', context)

def ReceiptDelivery2(request):
    context = {}
    return render(request,'wrh/ReceiptDelivery2.html', context)

def receipt_detail(request, pid):
    p2 = int(pid)
    try:
        clr = Clearance.objects.get(pk=p2)
        if clr.ready!='o':
            context = {'error':"کالاهای این حواله هنوز از انبار خارج نشده است."}
        else:
            if clr.type=='warehouse':
                context = {'error':"لطفا شماره حواله مربوط به سامانه فروش یا امور ویکی ها را وارد کنید."}
            context = {'clrs': clr}
    except Exception as e:
        context = {'error': "حواله ای با شماره داده شده یافت نشد."}
    return render(request, 'wrh/ReceiptDetail.html', context)

def confirm_receipt(request, pid):
    context = {}
    p2 = int(pid)
    try:
        clr = Clearance.objects.get(pk=p2)
        rcw = Receipt_Customer_Wiki(clearance = clr)
        rcw.save()
        if clr.type=='wiki':
            wk = clr.wiki
            wk.deliveryStatus = 2
            wk.save()
        else:
            if clr.type=='sale':
                bl = clr.bill
                bl.deliveryStatus = 2
                bl.save()
        context = {'msg': "رسید حواله انتخاب شده با موفقیت در سیستم ثبت شد."}
    except Exception as e:
        context = {'error': "حواله ای با شماره داده شده یافت نشد."}
    return render(request, 'wrh/ConfirmReceipt.html', context)
#****************************************END CUSTOMER WIKI RECEIPT***********************************
#**********************************************************************************************


#***********************************************************************************************************
#***********************************BEGIN MY FUNCS*******************************************************
def check_capacity():
    stocks = Stock.objects.all()
    capacity = 0
    for stock in stocks:
        capacity += (((stock.quantity) + (stock.quantity_returned))*(stock.product.volume))
    if capacity<(warehouse_capacity*0.6):
        return True
    else:
        return False

def check_order_point(pid):
    print("man to check order pointam")
    try:
        pr = Product.objects.get(pk = pid)
        wi = pr.wiki
        stc = Stock.objects.get(product = pr)
        if stc.quantity<order_point:
            if check_capacity():
                tmp = order_point-stc.quantity
                wo = Wiki_Order(product=pr , wiki=wi, quantity=tmp)
                wo.save()
    except Exception as e:
        wo = Wiki_Order(product=pr , wiki=wi, quantity=order_point)
        wo.save()
        print(str(e))

