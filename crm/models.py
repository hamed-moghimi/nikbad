# -*- encoding: utf-8 -*-
from django.db import models
from random import choice
from django.contrib.auth.models import User
from wiki.models import Product
gender_choices = (
                      ( 'm' , "مرد"),
                      ('f' , "زن")
                      )
    
# Create your models here.
class Customer (User):
    
    phone = models.CharField(max_length = 12 , verbose_name = u" شماره تلفن ثابت")
    gender = models.CharField(max_length = 1 , choices =  gender_choices ,verbose_name = u" جنسیت")
    postal_code = models.CharField (max_length = 10 , verbose_name = u"کدپستی" , blank = True )
    address = models.TextField( verbose_name = u" آدرس")
    city = models.CharField(max_length = 20 , verbose_name = u" شهر")


class Feedback (models.Model):
    date = models.DateField( auto_now_add=True , verbose_name = u" تاریخ بازخورد")
    content = models.TextField( verbose_name = u"متن بازخورد")
    product = models.ForeignKey(Product, verbose_name= u" نام کالا")
    