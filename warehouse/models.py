# -*- encoding: utf-8 -*-
from django.db import models

# Create your models here.
class Stock(models.Model):
    
    wiki = models.ForeignKey("wiki.models.wiki", verbose_name = u"ویکی")
    quantity_returned = models.IntegerField(verbose_name = u"مقدار مرجوعی")
    quantity = models.IntegerField(verbose_name = u"مقدار")
    rack_num_returned = models.IntegerField(verbose_name = u"شماره قفسه مرجوعی")
    rack_num = models.IntegerField(verbose_name = u"شماره قفسه")
    
    
class Reciept_Delivery(models.Model):
    
    wiki = models.ForeignKey("wiki.models.wiki", verbose_name = u"ویکی")
    product = models.ForeignKey("wiki.models.product" , verbose_name = u"کالا")
    quantity = models.IntegerField(verbose_name = u"مقدار")
    date = models.DateField(auto_now_add = True, verbose_name = u"تاریخ")
    
class Reciept_Return(models.Model):
    
    wiki = models.ForeignKey("wiki.models.wiki", verbose_name = u"ویکی")
    product = models.ForeignKey("wiki.models.product" , verbose_name = u"کالا")
    quantity = models.IntegerField(verbose_name = u"مقدار")
    date = models.DateField(auto_now_add = True, verbose_name = u"تاریخ")
    
class Receipt_Clearance(models.Model):
    
    date = models.DateField(auto_now_add = True, verbose_name = u"تاریخ")
    order = models.ForeignKey("sales.models.order", verbose_name = u"سفارش")
    
class Customer_Delivery(models.Model):
    
    date = models.DateField(auto_now_add = True, verbose_name = u"تاریخ")
    order = models.ForeignKey("sales.models.order", verbose_name = u"سفارش")
    
class Customer_Return(models.Model):
    
    date = models.DateField(auto_now_add = True, verbose_name = u"تاریخ")
    order = models.ForeignKey("sales.models.order", verbose_name = u"سفارش")
    product = models.ForeignKey("wiki.models.product" , verbose_name = u"کالا")


class Wiki_Order(models.Model):
    
    date = models.DateField(auto_now_add = True, verbose_name = u"تاریخ")
    product = models.ForeignKey("wiki.models.product" , verbose_name = u"کالا")
    wiki = models.ForeignKey("wiki.models.wiki", verbose_name = u"ویکی")
    quantity = models.IntegerField(verbose_name = u"مقدار")