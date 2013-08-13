# -*- encoding: utf-8 -*-
from fnc.models import Employee, RollCall, SalaryFactor, GeneralAccount, CostBenefit, WikiFactor
from datetime import timedelta, datetime
from sales.models import SaleBill_Product
from wiki.models import *


def payment_wiki():
    wikis = Wiki.objects.all()
    for w in wikis:
        payment = 0
        sb_ps = SaleBill_Product.objects.filter(SaleBill__SaleDate__gt = GeneralAccount.last_pay_wiki).filter(
            Product__Wiki = w)
        for x in sb_ps:
            payment += x.product.price * x.number
        payment = (payment * w.contract.percent) / 100
        w.payment, w.reminder = divmod(w.payment + w.reminder, 10000)
        w.save()
        wf = WikiFactor.objects.create(amount = w.payment, wiki = w)
        wf.save()
        GeneralAccount.getBudget().withdraw(payment)


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

        print "ep.hours.seconds ", ep.hours.seconds
        ep.payAmount, ep.reminderSalary = divmod(ep.hours.seconds * ep.salary + ep.reminderSalary, 36000000)
        print "pay amount ", ep.payAmount
        print "reminder ", ep.reminderSalary
        ep.save()
        totalPay += ep.payAmount
        sf = SalaryFactor.objects.create(amount = ep.payAmount, employee = ep)

    GeneralAccount.getBudget().withdraw(totalPay)


def make_cb_sb(sb):
    cb = CostBenefit()
    cb.bedeh = 0
    cb.bestan = sb.totalPrice
    cb.description = u'{0} {1}'.format(sb.customer.get_full_name, 'خرید توسط ')
    cb.save()
    cb.date = sb.saleDate
    cb.save()
    GeneralAccount.getBudget().deposit(cb.bestan)


def make_cb_contract(ct):
    cb = CostBenefit()
    cb.bedeh = 0
    cb.bestan = ct.fee
    cb.description = u'{0} {1}'.format(ct.wiki.companyName, '  آبونمان ویکی ')
    cb.save()
    GeneralAccount.getBudget().deposit(cb.bestan)