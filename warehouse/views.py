# -*- encoding: utf-8 -*-
from reportlab.lib.pagesizes import landscape, letter
from contrib.pdf import getPDF_Response, drawText
from contrib.pdf import PDFWriter, StringMark

from django.contrib.auth.decorators import permission_required, user_passes_test
from django.shortcuts import render
from sales.models import *
from wiki.models import *
from warehouse.models import *
from django.core.paginator import Paginator
import os

def perm_check(user):
    return user.has_perm('warehouse.is_mng_warehouse') or user.has_perm('warehouse.is_deliveryman')

@user_passes_test(perm_check)
def index(request):
    a = u'سامانه انار'
    context = {'name': a, 'request':request.get_full_path()}
    return render(request, 'wrh/base.html', context)

anbaargardaani_dif = []

#***********************************************************************************************************
#***********************************BEGIN NEW ORDERS*******************************************************
@permission_required('warehouse.is_warehouseman', login_url='index')
def new_order(request, org=""):
    title = "لیست حواله های انبار"
    panel = "*OrdersPanel"
    context = {'active_menu': 2, 'title':title, 'panel':panel, 'type':0}
    return render(request, 'wrh/Reports_Orders.html', context)

@permission_required('warehouse.is_warehouseman', login_url='index')
def order_panel(request, org = ""):
    first_msg = "حواله های جدید انبار به شرح زیر می باشند:"
    bill = SaleBill.objects.filter(deliveryStatus = 0)
    transference = Transference.objects.exclude(defective = 'r')
    wiki_return = ReturnRequest.objects.all()
    for b in bill:
        clear = Clearance.objects.filter(bill=b)
        if not clear:
            cl = Clearance(type='sale', date=b.saleDate, bill=b)
            cl.save()
    for tr in transference:
        clear = Clearance.objects.filter(transfer=tr)
        if not clear:
            cl = Clearance(type='warehouse', date=tr.date, transfer=tr)
            cl.save()
    for w in wiki_return:
        clear = Clearance.objects.filter(wiki=w)
        if not clear:
            cl = Clearance(type='wiki', date=w.pub_date, wiki=w)
            cl.save()

    clrs=Clearance.objects.filter(ready='n').order_by('date')
    if not clrs:
        first_msg = "حواله جدیدی در سیستم به ثبت نرسیده است."

    zipped = []
    for s in clrs:
        a = "*ReportDetail/"
        a += str(s.pk)
        a += "/9"
        zipped.append((s, a))

    # PAGINATION
    paginator = Paginator(zipped, 2)
    page = request.GET.get('page')
    print(page)
    try:
        contacts = paginator.page(page)
    except Exception as s:
        # If page is not an integer, deliver first page.
        print(str(s))
        contacts = paginator.page(1)

    add = "*OrdersPanel"
    context = {'clrs': contacts, 'active_menu': 2, 'first_msg':first_msg, 'paginator':paginator, 'contacts':contacts, 'lnk':add}
    return render(request, 'wrh/Orders-Panel.html', context)

@permission_required('warehouse.is_deliveryman', login_url='index')
def ready_order(request, org = ""):
    title = "لیست حواله های آماده خروج از انبار"
    panel = "*OrdersReadyPanel"
    context = {'active_menu': 12, 'title':title, 'panel':panel}
    return render(request, 'wrh/Reports_Orders.html', context)

@permission_required('warehouse.is_deliveryman', login_url='index')
def ready_order_panel(request, org = ""):
    first_msg = "حواله های آماده ترخیص به شرح زیر می باشند:"
    clrs = Clearance.objects.filter(ready='r').order_by('date')
    if not clrs:
        first_msg = "حواله جدیدی در سیستم به ثبت نرسیده است."

    zipped = []
    for s in clrs:
        a = "*ReportDetail/"
        a += str(s.pk)
        a += "/8"
        zipped.append((s, a))

    # PAGINATION
    paginator = Paginator(zipped, 2)
    page = request.GET.get('page')
    print(page)
    try:
        contacts = paginator.page(page)
    except Exception as s:
        # If page is not an integer, deliver first page.
        print(str(s))
        contacts = paginator.page(1)

    add = "*OrdersReadyPanel"
    context = {'clrs': contacts, 'active_menu': 12, 'first_msg':first_msg, 'paginator':paginator, 'contacts':contacts, 'lnk':add}
    return render(request, 'wrh/Orders-Panel.html', context)

@permission_required('warehouse.is_warehouseman', login_url='index')
def confirm_order(request, pid, org = ""):
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
        context = {'error': "این حواله به علت کمبود موجودی انبار آماده تحویل نیست.",'type':0, 'button':"بازگشت به لیست حواله ها"}
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
        context = {'msg': "کالاهای موجود در حواله انتخاب شده، آماده خروج از انبار هستند.", 'button':"بازگشت به لیست حواله ها"}
    return render(request, 'wrh/Confirm.html', context)

@permission_required('warehouse.is_deliveryman', login_url='index')
def confirm_ready_order(request, pid, org = ""):
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
    context = {'msg': "این حواله با موفقیت از انبار خارج شد و سند خروج از انبار ثبت گردید.", 'button':"بازگشت به لیست حواله ها", 'type':1}
    return render(request, 'wrh/Confirm.html', context)
#****************************************END NEW ORDER*****************************************
#**********************************************************************************************

#***********************************************************************************************************
#***********************************BEGIN WAREHOUSE DELIVERY*******************************************************
@permission_required('warehouse.is_warehouseman', login_url='index')
def delivery_wiki_select(request, org =""):
    context = {'active_menu': 1}
    return render(request,'wrh/WRHDelivery.html', context)

@permission_required('warehouse.is_warehouseman', login_url='index')
def delivery_wiki_select2(request, org = ""):
    a = Wiki.objects.all()
    # PAGINATION
    paginator = Paginator(a, 12)
    page = request.GET.get('page')
    print(page)
    try:
        contacts = paginator.page(page)
    except Exception as s:
        # If page is not an integer, deliver first page.
        print(str(s))
        contacts = paginator.page(1)

    context = {'wikis': contacts, 'active_menu': 1,'paginator':paginator, 'contacts':contacts, 'lnk':"*WRHDelivery-Panel"}
    return render(request, 'wrh/WRHDelivery-Panel.html', context)

@permission_required('warehouse.is_warehouseman', login_url='index')
def delivery_product_select(request, pid, org = ""):
    wik = Wiki.objects.filter(pk=pid)
    a = Product.objects.filter(wiki=wik)
    zipped = []
    for pr in a:
        index = -1
        if pr.orderPoint == 0:
            zipped.append((pr, -1))
        else:
            zipped.append((pr, pr.orderPoint))
    context = {'products': zipped}
    return render(request,'wrh/WRHDelivery-next.html', context)

@permission_required('warehouse.is_warehouseman', login_url='index')
def confirm_wrh_delivery(request, org = ""):

    context = {}
    if request.method == 'POST':
        try:
            post = request.POST
            if check_capacity():

                qnts = {}
                vlms = {}
                ords = {}

                for key, value in post.iteritems():
                    if key[:4]=="qnt_":
                        num = int(key[4:])
                        qnts[str(num)] = int(value)
                    else:
                        if key[:7]=="volume_":
                            num = int(key[7:])
                            vlms[str(num)] = int(value)
                        else:
                            if key[:6] == "order_":
                                num = int(key[6:])
                                ords[str(num)] = int(value)
                error_num = 0
                for dic_key in qnts.keys():
                    if qnts[dic_key]>0:
                        try:
                            volume = vlms[dic_key]
                            if volume == 0:
                                error_num = 1
                            else:
                                try:
                                    ord = ords[dic_key]
                                    if ord == 0:
                                        error_num = 2
                                except:
                                    error_num = 0
                        except:
                            error_num = 0
                            try:
                                ord = ords[dic_key]
                                if ord == 0:
                                    error_num = 2
                            except:
                                error_num = 0

                if error_num == 2:
                    context = {'error':"به علت وارد نشدن نقطه سفارش برای کالای تحویلی، این کالاها در سیستم ثبت نگردیدند.", 'button':"ثبت کالاهای تحویلی", 'type':0}
                elif error_num == 1:
                    context = {'error': "به علت وارد نشدن حجم تخمینی برای کالای تحویلی، این کالاها در سیستم ثبت نگردیدند.", 'button':"ثبت کالاهای تحویلی",'type':0}
                else:
                    for dic_key in qnts.keys():
                        if qnts[dic_key]>0:
                            prd = Product.objects.get(pk=int(dic_key))
                            stck = Stock.objects.filter(product=prd)
                            wk = prd.wiki
                            vl = qnts[dic_key]
                            if vl:
                                if not stck:
                                    st = Stock(product=prd , quantity= vl, quantity_returned=0, rack_num_returned=0, rack_num=0 )
                                    st.save()
                                else:
                                    stck[0].quantity += qnts[dic_key]
                                    stck[0].save()
                                # age sefareshi va3 in kalaa dade budam be wiki hamaye in sefaresharo migam reside
                                wk_order = Wiki_Order.objects.filter(product=prd, deliveryStatus=0)
                                for w in wk_order:
                                    w.deliveryStatus = 2
                                    w.save()

                                receipt_del = Receipt_Delivery(wiki=wk, product=prd, quantity=vl)
                                receipt_del.save()
                    for dic_key in vlms.keys():
                        if vlms[dic_key]>0:
                            prd = Product.objects.get(pk=int(dic_key))
                            prd.volume = vlms[dic_key]
                            prd.save()
                    for dic_key in ords.keys():
                        if ords[dic_key]>0:
                            prd = Product.objects.get(pk=int(dic_key))
                            prd.orderPoint = ords[dic_key]
                            prd.save()
                            # order_points_products.append(prd)
                            # order_points_value.append(ords[dic_key])
                    context = {'msg':"کالاهای تحویلی مربوط به ویکی انتخاب شده با موفقیت در سیستم ثبت شدند.", 'button':"ثبت کالاهای جدید"}
            else:
                context = {'error': "ظرفیت انبار برای ورود کالاهای زیر کافی نیست.", 'button':"ثبت کالاهای جدید", 'type':0}
        except Exception as e:
            print(str(e))
    return render(request, 'wrh/Confirm.html', context)
#****************************************END WAREHOUSE DELIVERY***********************************
#**********************************************************************************************


#***********************************************************************************************************
#***********************************BEGIN CUSTOMER RETURN*******************************************************
@permission_required('warehouse.is_warehouseman', login_url='index')
def customer_return(request, org=""):
    context = {'active_menu': 3}
    return render(request, 'wrh/CustomerReturn.html', context)

@permission_required('warehouse.is_warehouseman', login_url='index')
def point_order(request, org=""):
    context = {'active_menu': 15}
    return render(request, 'wrh/ChangeOrderPoint.html', context)

@permission_required('warehouse.is_warehouseman', login_url='index')
def customer_return_panel(request, org =""):
    context = { 'active_menu': 3}
    return render(request, 'wrh/CustomerReturn-Panel.html', context)

@permission_required('warehouse.is_warehouseman', login_url='index')
def point_orders_panel(request, org =""):
    context = { 'active_menu': 15}
    return render(request, 'wrh/ChangeOrderPoint-Panel.html', context)

@permission_required('warehouse.is_warehouseman', login_url='index')
def customer_return_next(request,org = ""):
    context = {}
    if request.method == 'POST':
        try:
            post = request.POST
            error = ""
            for key, value in post.iteritems():
                if key=="code":
                    try:
                        p2 = int(value)
                    except:
                        error = "لطفا یک عدد برای کد حواله وارد کنید."
                elif key == "pcode":
                    try:
                        k2 = int(value)
                    except:
                        error = "لطفا یک عدد برای کد کالا وارد کنید."
            if error == "":
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
                                    context = {'error': "تعداد کالای مرجوعی از این نوع برای حواله انتخاب شده قبلا در سیستم به ثبت رسیده است."}
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
                                        context = {'error': "تعداد کالای مرجوعی از این نوع برای حواله انتخاب شده قبلا در سیستم به ثبت رسیده است."}
                                    else:
                                        context = {'clr': clr, 'product': pro3}
                            else:
                                context = {'error': "کالای معیوب از ویکی دربافت نمی شود."}
                    except Exception as e:
                        print(str(e))
                        context = {'error': "کالایی با شماره داده شده در این حواله یافت نشد."}
        except Exception as e:
            print(str(e))
            context = {'error': "حواله ای با شماره داده شده یافت نشد."}
    if error!="":
        context = {'error':error}
    return render(request, 'wrh/CustomerReturn-next.html', context)

@permission_required('warehouse.is_warehouseman', login_url='index')
def point_order_next(request,org = ""):
    context = {}
    if request.method == 'POST':
        try:
            post = request.POST
            error = ""
            for key, value in post.iteritems():
                if key == "pcode":
                    try:
                        k2 = int(value)
                    except:
                        error = "لطفا یک عدد برای کد کالا وارد کنید."
            if error == "":
                try:
                    pr = Product.objects.get(goodsID=k2)
                except Exception as e:
                    print(str(e))
                    context = {'error': "کالایی با شماره داده شده یافت نشد."}
        except Exception as e:
            print(str(e))
    if error!="":
        context = {'error':error}
    else:
        context = {'product':pr}
    return render(request, 'wrh/ChangeOrderPoint-next.html', context)

@permission_required('warehouse.is_warehouseman', login_url='index')
def point_order_next2(request,kid, org = ""):
    context = {}
    k2 = int(kid)
    try:
        pr = Product.objects.get(goodsID=k2)
    except Exception as e:
        print(str(e))
        context = {'error': "کالایی با شماره داده شده یافت نشد."}
    else:
        context = {'product':pr}
    return render(request, 'wrh/ChangeOrderPoint-next.html', context)


@permission_required('warehouse.is_warehouseman', login_url='index')
def customer_return_next2(request,pid, kid, org = ""):
    context = {}
    error = ""
    try:
        p2 = int(pid)
    except:
        error = "لطفا یک عدد برای کد حواله وارد کنید."
    try:
        k2 = int(kid)
    except:
        error = "لطفا یک عدد برای کد کالا وارد کنید."
    try:
        if error == "":
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
                                context = {'error': "تعداد کالای مرجوعی از این نوع برای حواله انتخاب شده قبلا در سیستم به ثبت رسیده است."}
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
                                    context = {'error': "تعداد کالای مرجوعی از این نوع برای حواله انتخاب شده قبلا در سیستم به ثبت رسیده است."}
                                else:
                                    context = {'clr': clr, 'product': pro3}
                        else:
                            context = {'error': "کالای معیوب از ویکی دربافت نمی شود."}
                except Exception as e:
                    print(str(e))
                    context = {'error': "کالایی با شماره داده شده در این حواله یافت نشد."}
    except Exception as e:
        print(str(e))
        context = {'error': "حواله ای با شماره داده شده یافت نشد."}
    if error!="":
        context = {'error':error}
    return render(request, 'wrh/CustomerReturn-next.html', context)

@permission_required('warehouse.is_warehouseman', login_url='index')
def confirm_return(request, pid, kid, cid,type, org = ""):
    context = {}
    clr_id = int(pid)
    pro_id = int(kid)
    qnt = int(cid)
    # tp = bool(type)
    if type == "true":
        tp = True
    else:
        tp = False
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
    if qnt==0:
        context = {'error':"لطفا عددی بزرگتر از صفر برای مقدار کالای معیوب وارد کنید.",'pid':pid, 'kid':kid, 'type':2}
    elif quan<qnt:
        context={'error': "مقدار وارد شده برای کالای مرجوعی بیش تر از مقدار ثبت شده در حواله است.", 'pid':pid, 'kid':kid, 'type':2}
    else:
        try:
            stck= Stock.objects.get(product=p2)
            if tp:
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
                context = {'msg': "کالاهای مرجوعی به موجودی انبار اضافه شده و تحویل آن ها در سیستم ثبت گردید.", 'button':"ثبت مرجوعی جدید"}
            else:
                stck.quantity += qnt
                receipt_del = Receipt_Delivery(wiki=(p2.wiki), product=p2, quantity=qnt)
                receipt_del.save()
                if clr.type=='warehouse':
                    t = clr.transfer
                    t.defective = 'd'
                    t.save()
                else:
                    if clr.type == 'warehouse':
                        tr = Transference(bill=(clr.transfer.bill), product=p2, quantity=qnt, defective = 'r')
                        tr.save()

                context = {'msg': "کالاهای معیوب با موفقیت در لیست کالاهای مرجوعی ثبت شده و حواله جدید برای ارسال مجدد کالا صادر گردید.", 'button':"ثبت مرجوعی جدید"}
            stck.save()
        except Exception as e:
            print(str(e))
    return render(request, 'wrh/Confirm.html', context)

@permission_required('warehouse.is_warehouseman', login_url='index')
def confirm_order_point(request, kid, cid, org = ""):
    context = {}
    pro_id = int(kid)
    qnt = int(cid)
    pr = Product.objects.get(goodsID=pro_id)

    if qnt==0:
        context = {'error':"لطفا عددی بزرگتر از صفر برای مقدار نقطه سفارش وارد کنید.", 'kid':kid, 'type':1}
    else:
        pr .orderPoint = qnt
        pr.save()
        context = {'msg': "نقطه سفارش با موفقیت برای کالای انتخاب شده ثبت گردید.", 'button':"ثبت نقطه سفارش جدید"}
    return render(request, 'wrh/Confirm.html', context)
#****************************************END CUSTOMER RETURN***********************************
#**********************************************************************************************

#***********************************************************************************************************
#***********************************BEGIN CUSTOMER WIKI RECEIPT*******************************************************
@permission_required('warehouse.is_deliveryman', login_url='index')
def ReceiptDelivery(request, org= ""):
    context = {}
    return render(request,'wrh/ReceiptDelivery.html', context)

@permission_required('warehouse.is_deliveryman', login_url='index')
def ReceiptDelivery_Panel(request, org = ""):
    first_msg = "لطفا شماره حواله تحویل داده شده را وارد کنید:"
    context = {'first_msg':first_msg}
    return render(request, 'wrh/ReceiptDelivery-Panel.html', context)

@permission_required('warehouse.is_deliveryman', login_url='index')
def receipt_detail(request,org = ""):
    context = {}
    if request.method == 'POST':
        try:
            post = request.POST
            error = ""
            for key, value in post.iteritems():
                if key=="code":
                    try:
                        p2 = int(value)
                    except:
                        error = "لطفا یک عدد برای کد حواله وارد کنید."
            if error == "":
                clr = Clearance.objects.get(pk=p2)
                if clr.ready!='o':
                    context = {'error':"کالاهای این حواله هنوز از انبار خارج نشده است."}
                else:
                    if clr.type=='warehouse':
                        context = {'error':"لطفا شماره حواله مربوط به سامانه فروش یا امور ویکی ها را وارد کنید."}
                    else:
                        if clr.type == 'sale':
                            if clr.bill.deliveryStatus == 2:
                                context = {'error': "رسید این حواله قبلا در سیستم به ثبت رسیده است."}
                            else:
                                context = {'clrs': clr, 'src':10}
                        else:
                            if clr.wiki.deliveryStatus == 2:
                                context = {'error': "رسید این حواله قبلا در سیستم به ثبت رسیده است."}
                            else:
                                context = {'clrs': clr, 'src':10}
        except Exception as e:
            print(str(e))
            context = {'error': "حواله ای با شماره داده شده یافت نشد."}
    if error!="":
        context = {'error':error}
    return render(request, 'wrh/ReportDetail.html', context)

@permission_required('warehouse.is_deliveryman', login_url='index')
def confirm_receipt(request, pid, org = ""):
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
        context = {'msg': "رسید حواله انتخاب شده با موفقیت در سیستم ثبت شد.", 'button':"ثبت رسید جدید", 'type': 0}
    except Exception as e:
        context = {'error': "حواله ای با شماره داده شده یافت نشد.", 'button':"ثبت رسید جدید", 'type': 0}
    return render(request, 'wrh/Confirm.html', context)
#****************************************END CUSTOMER WIKI RECEIPT***********************************
#**********************************************************************************************

#***********************************************************************************************************
#***********************************BEGIN REPORTS***********************************************************
@permission_required('warehouse.is_mng_warehouse', login_url='index')
def reports(request, menu_id, org=""):
    tmp = int(menu_id)
    title = titles[tmp]
    panel = ""
    if (tmp >= 4) and (tmp <= 7):
        panel = "ReportProduct_Panel/"
        panel += str(tmp)
    elif (tmp >= 8) and (tmp <= 11):
        panel = "ReportReceipt_Panel/"
        panel += str(tmp)
    elif tmp == 14:
        panel = "ReportReceiptDelivery_Panel"
    elif tmp == 16:
        panel = "WRHgardani-Panel"
    context = {'active_menu' : tmp, 'title': title , 'panel':panel}
    return render(request, 'wrh/Reports_Orders.html', context)

@permission_required('warehouse.is_mng_warehouse', login_url='index')
def wrh_gardaani(request, org=""):
    prs = Product.objects.all()
    context = {'products': prs}
    return render(request, 'wrh/WRHgardani-Panel.html', context)

@permission_required('warehouse.is_mng_warehouse', login_url='index')
def printt(request, org=""):
    prs = Product.objects.all()
    a = [
            [
            ],
        ]
    i = 0
    j = 0

    for pr in prs:
        a[j].append(StringMark(497 + len(str(pr.goodsID))*3, -40 + i, pr.goodsID))
        a[j].append(StringMark(425 + len(u''.join(pr.name))*3, -40 + i, u''.join(pr.name)))
        a[j].append(StringMark(370 + len(str(pr.wiki.pk))*3, -40 + i, pr.wiki.pk))
        a[j].append(StringMark(297 + len(u''.join(pr.wiki.companyName))*3, -40 + i, u''.join(pr.wiki.companyName)))
        a[j].append(StringMark(100 + len(u''.join(pr.unit))*2, -40 + i, u''.join(pr.unit)))
        i += 20
        if i == 20*28:
            j +=1
            a.append([])
            i = 0
    return getPDF_Response(a, os.path.join(settings.MEDIA_ROOT, 'PDFs/anbaargardani.pdf'), pageSize = letter,   orientation = landscape)

@permission_required('warehouse.is_mng_warehouse', login_url='index')
def print_dif(request, org=""):
    a = [
        [
        ],
    ]
    i = 0
    j = 0

    for pr, pk, cnt, cal,dif, type in anbaargardaani_dif:
        a[j].append(StringMark(517 + len(str(pr.goodsID))*3, -7 + i, pr.goodsID))
        a[j].append(StringMark(460 + len(u''.join(pr.name))*2.5, -7 + i, u''.join(pr.name)))
        a[j].append(StringMark(406 + len(str(pr.wiki.pk))*3, -7 + i, pr.wiki.pk))
        a[j].append(StringMark(350 + len(u''.join(pr.wiki.companyName))*3, -7 + i, u''.join(pr.wiki.companyName)))
        a[j].append(StringMark(295 + len(str(cnt))*3, -7 + i, cnt))
        a[j].append(StringMark(245 + len(str(cal))*3, -7 + i, cal))
        a[j].append(StringMark(200 + len(u''.join(pr.unit))*1.5, -7 + i, u''.join(pr.unit)))
        a[j].append(StringMark(143 + len(str(dif))*3, -7 + i, dif))
        if type==1:
            a[j].append(StringMark(94 + len(u'معیوب')*1.5, -7 + i, u'معیوب'))
        else:
            a[j].append(StringMark(94 + len(u'سالم')*1.5, -7 + i, u'سالم'))
        i += 20
        if i == 20*28:
            j +=1
            a.append([])
            i = 0
    return getPDF_Response(a, os.path.join(settings.MEDIA_ROOT, 'PDFs/anbaargardaani-dif.pdf'), pageSize = letter,   orientation = landscape)


@permission_required('warehouse.is_mng_warehouse', login_url='index')
def wrh_gardaani_confirm(request, org=""):
    context = {}
    del anbaargardaani_dif[0:len(anbaargardaani_dif)]

    if request.method == 'POST':
        try:
            post = request.POST
            qnts = {}
            qnts_dmgd = {}

            for key, value in post.iteritems():
                if key[:4]=="qnt_":
                    num = int(key[4:])
                    qnts[str(num)] = int(value)
                else:
                    if key[:5]=="dmgd_":
                        num = int(key[5:])
                        qnts_dmgd[str(num)] = int(value)

            tmp = [] #3 meghdarre product , meghdare shomaresh shodeye product va meghdare mohasebe shodeye tedad + no ( yani saalem ya mayub)
            for dic_key in qnts:
                pr = Product.objects.get(goodsID=int(dic_key))
                stc = Stock.objects.filter(product = pr)
                if not stc:
                    if qnts[dic_key]>0:
                        tmp.append((pr,pr.pk,qnts[dic_key],0,qnts[dic_key],0))
                else:
                    if stc[0].quantity != qnts[dic_key]:
                        tmp.append((pr, pr.pk,qnts[dic_key], stc[0].quantity,qnts[dic_key]-stc[0].quantity, 0))

            for dic_key in qnts_dmgd:
                pr = Product.objects.get(goodsID=int(dic_key))
                stc = Stock.objects.filter(product = pr)
                if not stc:
                    if qnts_dmgd[dic_key]>0:
                        tmp.append((pr,pr.pk,qnts_dmgd[dic_key],0,qnts_dmgd[dic_key],1))
                else:
                    if stc[0].quantity_returned != qnts_dmgd[dic_key]:
                        tmp.append((pr, pr.pk,qnts_dmgd[dic_key], stc[0].quantity_returned,qnts_dmgd[dic_key]-stc[0].quantity_returned, 1))
        except Exception as s:
            print(str(s))

    tmp.sort(key=lambda tup: tup[1])
    for t in tmp:
        anbaargardaani_dif.append(t)
    context = {'products': tmp}
    return render(request, 'wrh/WRHGardaani-next.html', context)

@permission_required('warehouse.is_mng_warehouse', login_url='index')
def report_receipt_panel(request, menu_id, org="", num =0):
    tmp = int(menu_id)
    if tmp == 8:
        st = Receipt_Clearance.objects.all().order_by('-date')
        first_msg = "ترخیص های انبار به شرح زیر می باشند:"
        if not st:
            first_msg = "هنوز هیچ ترخیصی از انبار صورت نگرفته است."
    elif tmp == 9:
        st = Receipt_Customer_Wiki.objects.filter(clearance__in=Clearance.objects.filter(type='sale')).order_by('-date')
        first_msg = "رسیدهای کالا به مشتریان به شرح زیر می باشند:"
        if not st:
            first_msg = "هنوز هیچ رسیدی برای تحویل کالا به مشتریان به ثبت نرسیده است."
    elif tmp == 10:
        st = Receipt_Customer_Wiki.objects.filter(clearance__in=Clearance.objects.filter(type='wiki')).order_by('-date')
        first_msg = "رسیدهای کالا به ویکی ها به شرح زیر می باشند:"
        if not st:
            first_msg = "هنوز هیچ رسیدی برای تحویل کالا به ویکی ها به ثبت نرسیده است."
    else:
        first_msg = "حواله های انبار به شرح زیر می باشند:"
        bill = SaleBill.objects.filter(deliveryStatus = 0)
        transference = Transference.objects.exclude(defective = 'r')
        wiki_return = ReturnRequest.objects.filter(deliveryStatus = 0)
        for b in bill:
            clear = Clearance.objects.filter(bill=b)
            if not clear:
                cl = Clearance(type='sale', date=b.saleDate, bill=b)
                cl.save()
        for tr in transference:
            clear = Clearance.objects.filter(transfer=tr)
            if not clear:
                cl = Clearance(type='warehouse', date=tr.date, transfer=tr)
                cl.save()
        for w in wiki_return:
            clear = Clearance.objects.filter(wiki=w)
            if not clear:
                cl = Clearance(type='wiki', date=w.pub_date, wiki=w)
                cl.save()

        st=Clearance.objects.all().order_by('-date')
        if not st:
            first_msg = "هنوز هیچ حواله ای برای انبار به ثبت نرسیده است."
    zipped = []
    if tmp == 11:
        for s in st:
            a = "*ReportDetail/"
            a += str(s.pk)
            a += "/"
            a += str((tmp-7))
            zipped.append((s, a))
    else:
        for s in st:
            a = "*ReportDetail/"
            a += str(s.clearance.pk)
            a += "/"
            a += str((tmp-7))
            zipped.append((s, a))

    # PAGINATION
    paginator = Paginator(zipped, 2)
    page = request.GET.get('page')
    print(page)
    try:
        contacts = paginator.page(page)
    except Exception as s:
        # If page is not an integer, deliver first page.
        print(str(s))
        contacts = paginator.page(1)

    add = "ReportReceipt_Panel/"
    add += str(tmp)
    context = {'dls': contacts, 'active_menu' : tmp, 'first_msg':first_msg, 'paginator':paginator, 'contacts':contacts, 'lnk':add}
    return render(request, 'wrh/ReportReceipt-Panel.html', context)

@permission_required('warehouse.is_mng_warehouse', login_url='index')
def report_product_panel(request, menu_id, org="", num = 0):

    tmp = int(menu_id)
    if tmp == 4:
        first_msg = "کالاهای موجود در انبار به شرح زیر می باشند:"
        st = Stock.objects.filter(quantity__gt=0).order_by('product__goodsID')
        if not st:
            first_msg = "انبار خالی است."
    elif tmp== 5:
        first_msg = "کالاهای معیوب موجود در انبار به شرح زیر می باشند:"
        st = Stock.objects.filter(quantity_returned__gt=0).order_by('product__goodsID')
        if not st:
            first_msg = "انبار کالای معیوب ندارد."
    elif tmp == 6:
        first_msg = "سفارشات انبار به شرح زیر می باشند:"
        st = Wiki_Order.objects.all().order_by('-date')
        if not st:
            first_msg = "هیچ سفارشی برای ویکی ها از طرف انبار به ثبت نرسیده است."
    else:
        first_msg = "تحویل های انبار به شرح زیر می باشند:"
        st = Receipt_Delivery.objects.all().order_by('-date')
        if not st:
            first_msg = "هیچ تحویل کالایی برای انبار به ثبت نرسیده است."

    # PAGINATION
    paginator = Paginator(st, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except Exception as s:
        # If page is not an integer, deliver first page.
        print(str(s))
        contacts = paginator.page(1)

    context = {'stocks': contacts, 'active_menu' : tmp,'first_msg':first_msg, 'paginator':paginator, 'contacts':contacts}
    return render(request, 'wrh/ReportProduct-Panel.html', context)

@permission_required('warehouse.is_deliveryman', login_url='index')
def report_receipt_delivery(request, org =""):
    title = "گزارش  رسیدهای ثبت شده"
    panel = "*ReportReceiptDelivery_Panel"
    context = {'active_menu' : 14, 'title': title, 'panel':panel}
    return render(request, 'wrh/Reports_Orders.html', context)

@permission_required('warehouse.is_deliveryman', login_url='index')
def report_receipt_delivery2(request, org="", num = 0):
    st = Receipt_Customer_Wiki.objects.all().order_by('-date')
    zipped = []
    for s in st:
        a = "*ReportDetail/"
        a += str(s.clearance.pk)
        a += "/7"
        zipped.append((s, a))

    # PAGINATION
    paginator = Paginator(zipped, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except Exception as s:
        # If page is not an integer, deliver first page.
        print(str(s))
        contacts = paginator.page(1)

    add = "*ReportReceiptDelivery_Panel"
    first_msg = "                    رسیدهای ثبت شده به شرح زیر می باشند:"
    if not st:
        first_msg = "هنوز هیچ رسیدی به ثبت نرسیده است."
    context = {'dls': contacts, 'active_menu' : 8, 'first_msg':first_msg, 'lnk':add,'paginator':paginator, 'contacts':contacts}
    return render(request, 'wrh/ReportReceipt-Panel.html', context)

def report_detail(request, pid, kid, org = ""):
    p2 = int(pid)
    k2 = int(kid)
    a = Clearance.objects.get(pk=p2)
    context = {'clrs': a, 'src':k2}
    return render(request, 'wrh/ReportDetail.html', context)
#****************************************END REPORTS*********************************************
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
    try:
        pr = Product.objects.get(pk = pid)
        wi = pr.wiki
        stc = Stock.objects.get(product = pr)
        if (stc.quantity-stc.reserved_quantity)<pr.orderPoint:
            if check_capacity():
                tmp = pr.orderPoint-(stc.quantity-stc.reserved_quantity)+10
                wk_tmp = Wiki_Order.objects.filter(product=pr , deliveryStatus=0)
                if wk_tmp.all():
                    print("ye chizi")
                else:
                    wo = Wiki_Order(product=pr , wiki=wi, quantity=tmp)
                    wo.save()
    except Exception as e:
        wk_tmp = Wiki_Order.objects.filter(product=pr , deliveryStatus=0)
        if wk_tmp.all():
            print("ye chizi")
        else:
            wo = Wiki_Order(product=pr , wiki=wi, quantity=(pr.orderPoint+10))
            wo.save()
        print(str(e))


titles = {
    4: "گزارش موجودی انبار",
    5: "گزارش مرجوعی های انبار",
    6: "گزارش  سفارشات انبار",
    7: "گزارش  تحویل های انبار",
    8: "گزارش  ترخیص های انبار",
    9: "گزارش  رسیدهای کالا به مشتریان",
    10: "گزارش  رسیدهای کالا به ویکی ها",
    11:"گزارش  حواله های انبار",
    16:"انبارگردانی",
}

