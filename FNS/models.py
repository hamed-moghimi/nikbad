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
	employee_id = models.CharField(max_length=200,verbose_name=u"????? ??????")
	date = models.DateField(auto_now_add=True, verbose_name=u"?????")
	entrance_time = models.DateField(auto_now_add=True, verbose_name=u"???? ????")
	exit_time = models.DateField(auto_now_add=True, verbose_name=u"???? ????")


class CostBenefit(models.Model):
	id = models.CharField(max_length=200,verbose_name=u"?????")
	date = models.DateField(auto_now_add=True, verbose_name=u"?????")
	description= models.TextField(verbose_name=u"???????")
	amount= models.PositiveIntegerField(verbose_name=u"?????")


class Employee(models.Model):
	id = models.CharField(max_length=200,verbose_name=u"?????")
	name = models.CharField(max_length=200,verbose_name=u"???")
	family_name = models.CharField(max_length=200,verbose_name=u"??? ????????")
	national_id = models.CharField(max_length=200,verbose_name=u"????? ???")
	mobile_num = models.CharField(max_length=200,verbose_name=u"شماره ملی")
	tel_num = models.CharField(max_length=200,verbose_name=u"شماره ملی")
	address = models.CharField(max_length=200,verbose_name=u"????")
	marriage_status = models.CharField(max_length=200,verbose_name=u"????? ????")
	salary= models.PositiveIntegerField(verbose_name=u"????")