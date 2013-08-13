# -*- encoding: utf-8 -*-
from fnc.models import Employee, RollCall, SalaryFactor, GeneralAccount, CostBenefit, WikiFactor
from datetime import timedelta, datetime
from sales.models import SaleBill_Product
from wiki.models import *

def payment_wiki():
	wikis=Wiki.objects.all()
	for w in wikis:
		payment=0
		sb_ps=SaleBill_Product.objects.filter(bill__saleDate__gt = GeneralAccount.getBudget().last_pay_wiki).filter(product__wiki=w)
		for x in sb_ps:
			payment+=x.product.price*x.number
		payment= (payment*w.contract.percent)/100
		w.payment, w.reminder = divmod(payment + w.reminder, 100)
		w.save()
		wf = WikiFactor.objects.create(amount=w.payment, wiki=w)
		wf.save()
		make_cb_wf(wf)
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
			ep.hours += exit-enter
		#ep.hours=ep.hours.seconds/3600
		q, r = divmod(ep.hours.seconds * ep.salary + ep.reminderSalary, 3600)
		ep.payAmount, ep.reminderSalary = divmod(q, 100)
		ep.payAmount=ep.payAmount*100
		print "pay amount ", ep.payAmount
		print "reminder " , ep.reminderSalary
		ep.save()
		totalPay += ep.payAmount
		sf = SalaryFactor.objects.create(amount=ep.payAmount, employee=ep)
		make_cb_sf(sf)

	GeneralAccount.getBudget().withdraw(totalPay)


def make_cb_sb(sb):
	cb = CostBenefit()
	cb.bedeh=0
	cb.bestan= sb.totalPrice
	cb.description= u'{0} {1}'.format(sb.customer.get_full_name,'خرید توسط ')
	cb.save()
	cb.date=sb.saleDate
	cb.save()
	GeneralAccount.getBudget().deposit(cb.bestan)
	print "sale bill done"

def make_cb_contract (ct):
	cb = CostBenefit()
	cb.bedeh=0
	cb.bestan= ct.fee
	cb.description= u'{0} {1}'.format(u'  آبونمان ویکی ',ct.wiki.companyName)
	cb.save()
	GeneralAccount.getBudget().deposit(cb.bestan)
	print "got wiki abonman"

def make_cb_sf(sf):
	cb = CostBenefit()
	cb.bedeh= sf.amount
	cb.bestan= 0
	cb.description= u'{0} {1}'.format(u'  پرداخت حقوق ',sf.employee)
	cb.save()
	print "employee payment done"

def make_cb_wf(wf):
	cb = CostBenefit()
	cb.bedeh= wf.amount
	cb.bestan= 0
	cb.description= u'{0} {1}'.format(u' پرداخت سهم ویکی ',wf.wiki)
	cb.save()
	print "wiki payment done"
