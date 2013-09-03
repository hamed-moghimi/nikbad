# -*- encoding: utf-8 -*-
from django.utils import timezone
from fnc.models import *
from datetime import timedelta, datetime
from sales.models import SaleBill_Product
from wiki.models import *

#pay wiki / should be invoked monthly
def payment_wiki():
    wikis = Wiki.objects.all()
    budget = GeneralAccount.getBudget()

    for w in wikis:
        total = 0
        sb_ps = SaleBill_Product.objects.filter(bill__saleDate__gt=budget.last_pay_wiki).filter(product__wiki=w)
        for x in sb_ps:
            total += x.product.price * x.number
        payment = total * (100 - w.contract.percent) / 100
        benefit=total-payment
        make_benefit(benefit, w)
        w.payment, w.reminder = divmod(payment + w.reminder, 100)
        w.payment *= 100
        w.save()
        wf = WikiFactor.objects.create(amount=w.payment, wiki=w)
        wf.save()
        make_cb_wf(wf)
        budget.withdraw(payment)

    budget.last_pay_wiki = timezone.now()
    budget.save()

#pay employees / should be invoked monthly
def payment_emp():
    employees = Employee.objects.all()
    totalPay = 0
    for ep in employees:
        rollcalls = ep.rollCalls.all()
        ep.hours = timedelta()
        for rc in rollcalls:
            enter = datetime.combine(rc.date, rc.entrance_time)
            exit = datetime.combine(rc.date, rc.exit_time)
            ep.hours += exit - enter
            #ep.hours=ep.hours.seconds/3600
        q, r = divmod(ep.hours.seconds * ep.salary + ep.reminderSalary, 3600)
        ep.payAmount, ep.reminderSalary = divmod(q, 100)
        ep.payAmount = ep.payAmount * 100
        print "pay amount ", ep.payAmount
        print "reminder ", ep.reminderSalary
        ep.save()
        totalPay += ep.payAmount
        sf = SalaryFactor.objects.create(amount=ep.payAmount, employee=ep)
        #make_cb_sf(sf)
        sf.save()

    make_cb_emp(totalPay)
    budget = GeneralAccount.getBudget()
    budget.withdraw(totalPay)
    budget.last_pay_emp = timezone.now()
    budget.save()


def make_cb_sb(sb):
    daramad=Account.objects.get(name=u"درآمد")
    darayi=Account.objects.get(name=u"دارایی")
    cb = CostBenefit()

    cb.account_bedeh=darayi
    cb.amount = sb.totalPrice
    darayi.deposit(sb.totalPrice)
    darayi.save()

    cb.account_bestan=daramad
    cb.amount = sb.totalPrice
    daramad.withdraw(sb.totalPrice)
    daramad.save()

    cb.description = u'{0} {1}'.format(u'خرید توسط ', sb.customer.get_full_name())
    cb.date = sb.saleDate
    cb.save()
   # GeneralAccount.getBudget().deposit(cb.bestan)
    print "sale bill done"


def make_cb_contract(ct):
    daramad=Account.objects.get(name=u"درآمد")
    darayi=Account.objects.get(name=u"دارایی")
    cb = CostBenefit()

    cb.account_bedeh = darayi
    cb.amount = ct.fee
    darayi.deposit(ct.fee)
    darayi.save()

    cb.account_bestan = daramad
    cb.amount= ct.fee
    daramad.withdraw(ct.fee)
    daramad.save()

    cb.description = u'{0} {1}'.format(u'  آبونمان ویکی ', ct.wiki.companyName)
    cb.save()
   # GeneralAccount.getBudget().deposit(cb.bestan)
    print "got wiki abonman"


#def make_cb_sf(sf):
# cb = CostBenefit()
# cb.bedeh = sf.amount
# cb.bestan = 0
# cb.description = u'{0} {1}'.format(u'  پرداخت حقوق ', sf.employee)
# cb.save()
#print "employee payment done"


def make_cb_wf(wf):
    hazine=Account.objects.get(name=u"هزینه")
    darayi= Account.objects.get(name=u"دارایی")
    cb = CostBenefit()

    cb.account_bedeh = hazine
    cb.amount = wf.amount
    hazine.deposit(wf.amount)
    hazine.save()

    cb.account_bestan= darayi
    cb.bestan = wf.amount
    darayi.withdraw(wf.amount)
    darayi.save()

    cb.description = u'{0} {1}'.format(u' پرداخت سهم ویکی ', wf.wiki)
    cb.save()
    print "wiki payment done"


def make_cb_emp(totalPay):
    hazine=Account.objects.get(name=u"هزینه")
    darayi= Account.objects.get(name=u"دارایی")
    cb = CostBenefit()

    cb.account_bedeh= hazine
    cb.amount = totalPay
    hazine.deposit(totalPay)
    hazine.save()

    cb.account_bestan = darayi
    cb.amount = totalPay
    darayi.withdraw(totalPay)
    darayi.save()

    cb.description = u"پرداخت حقوق کارمندان"
    cb.save()

# this function makes taraz, should be invoked each month
def tarazname():
    taraz = Taraz()
    taraz.save()
    accounts= Account.objects.all()
    for acc in accounts:
        row = Row()
        cb_bedeh = CostBenefit.objects.filter(account_bedeh=acc)
        for cb in cb_bedeh:
            row.gardesh_bedeh += cb.amount
        cb_bestan = CostBenefit.objects.filter(account_bestan=acc)
        for cb in cb_bestan:
            row.gardesh_bestan += cb.amount
        mande = row.gardesh_bedeh - row.gardesh_bestan

        if (mande > 0):
            row.mande_bedeh = mande
            row.mande_bestan = 0
        else:
            row.mande_bedeh = 0
            row.mande_bestan = -mande

        row.account=acc
        row.taraz=taraz
        row.save()

def make_benefit(benefit, wiki):
    daramad=Account.objects.get(name=u"درآمد")
    darayi=Account.objects.get(name=u"دارایی")
    cb = CostBenefit()

    cb.account_bedeh = darayi
    cb.amount = benefit
    darayi.deposit(benefit)
    darayi.save()

    cb.account_bestan = daramad
    cb.amount=benefit
    daramad.withdraw(benefit)
    daramad.save()

    cb.description = u'{0} {1}'.format(u'سهم سراب از فروش محصولات', wiki.companyName)
    cb.save()

# this function is invoked each year
def final_fnc():
    daramad=Account.objects.get(name=u"درآمد")
    hazine=Account.objects.get(name=u"هزینه")

    darayi=Account.objects.get(name=u"دارایی")

    sood= daramad.amount- hazine.amount
    darayi.amount+=sood
    darayi.save()
    daramad.amount=0
    daramad.save()
    hazine.amount=0
    hazine.save()


