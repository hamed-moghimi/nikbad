# -*- encoding: utf-8 -*-
from django.db import models


relation_choices= (('s',"????"),('m',"?"))

# Create your models here.
class Message(models.Model):
	message = models.CharField(max_length=200)
	date = models.DateTimeField()
	#user_from = models.ForeignKey(User, related_name="sent")
	#user_to = models.ForeignKey(User, related_name="received")



class RollCall(models.Model):
	employee_id = models.CharField(max_length=200,verbose_name=u"شناسه کارمند")
	date = models.DateField(auto_now_add=True, verbose_name=u"تاریخ")
	entrance_time = models.DateField(auto_now_add=True, verbose_name=u"زمان ورود")
	exit_time = models.DateField(auto_now_add=True, verbose_name=u"زمان خروج")


class CostBenefit(models.Model):
	date = models.DateField(auto_now_add=True, verbose_name=u"تاریخ")
	description= models.TextField(verbose_name=u"جزئیات")
	bedeh= models.PositiveIntegerField(verbose_name=u"بدهکاری")
	bestan= models.PositiveIntegerField(verbose_name=u"بستانکاری")


class Employee(models.Model):
	name = models.CharField(max_length=200,verbose_name=u"نام")
	family_name = models.CharField(max_length=200,verbose_name=u"نام خانوادگی")
	national_id = models.CharField(max_length=200,verbose_name=u"شماره ملی")
	mobile_num = models.CharField(max_length=200,verbose_name=u"شماره همراه")
	tel_num = models.CharField(max_length=200,verbose_name=u"شماره تلفن")
	address = models.CharField(max_length=200,verbose_name=u"آدرس")
	marriage_status = models.CharField(max_length=200,verbose_name=u"وضعیت تاهل")
	salary= models.PositiveIntegerField(verbose_name=u"حقوق")

class SalaryFactor(models.Model):
	date = models.DateField(auto_now_add=True, verbose_name=u"تاریخ")
	amount= models.PositiveIntegerField(verbose_name=u"مقدار")
