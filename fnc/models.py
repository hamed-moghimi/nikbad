# -*- encoding: utf-8 -*-
from django.db import models

relation_choices= (('s',"متاهل"),('m',"مجرد"))

class RollCall(models.Model):
	date = models.DateField(auto_now_add=True, verbose_name=u"تاریخ")
	entrance_time = models.TimeField( verbose_name=u"زمان ورود")
	exit_time = models.TimeField( verbose_name=u"زمان خروج")
	employee = models.ForeignKey('Employee', related_name = 'rollCalls')



class CostBenefit(models.Model):
	date = models.DateField(auto_now_add=True, verbose_name=u"تاریخ")
	description= models.TextField(verbose_name=u"جزئیات")
	bedeh= models.IntegerField(verbose_name=u"بدهکاری",  null=True, blank=True)
	bestan= models.IntegerField(verbose_name=u"بستانکاری", null=True, blank=True)
	generalAccount=models.ForeignKey('GeneralAccount', related_name='costBenefits', null=True, blank=True)

class GeneralAccount(models.Model):
	bedeh= models.IntegerField(verbose_name=u"بدهکاری")
	bestan= models.IntegerField(verbose_name=u"بستانکاری")
	description= models.TextField(verbose_name=u"اسم")

class Employee(models.Model):
	name = models.CharField(max_length=200,verbose_name=u"نام")
	family_name = models.CharField(max_length=200,verbose_name=u"نام خانوادگی")
	national_id = models.CharField(max_length=200,verbose_name=u"شماره ملی")
	mobile_num = models.CharField(max_length=200,verbose_name=u"شماره همراه")
	tel_num = models.CharField(max_length=200,verbose_name=u"شماره تلفن")
	address = models.TextField(verbose_name=u"آدرس")
	marriage_status = models.CharField(max_length=200,verbose_name=u"وضعیت تاهل",choices=relation_choices)
	salary= models.IntegerField(verbose_name=u"حقوق")

	def __unicode__(self):
		return u'{0} - {1}'.format(self.name, self.family_name)

class SalaryFactor(models.Model):
	date = models.DateField(auto_now_add=True, verbose_name=u"تاریخ")
	amount= models.IntegerField(verbose_name=u"مقدار")
	employee = models.ForeignKey(Employee, related_name = 'salaryFactors')
