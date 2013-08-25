# -*- encoding: utf-8 -*-
from django.db import models
from wiki.models import *
from sales.models import SaleBill

warehouse_capacity = 300000000 # cm^3
order_point = 20 # noghte sefaresh

# noe havaaleye anbaar
clear_type = (
    ('sale', u'فروش'),
    ('wiki', u'ویکی'),
    ('warehouse', u'انبار')
)

# kalaa amadeye tarxis hast ya na -> ezafe shod ke az anbar xarej shode ya na va3 inke mayoub va3 chizi ke xarej nashode sabt nashe
ready = {
    ('r', 'ready'),
    ('n', 'not_ready'),
    ('o', 'out')
}

# va3 in gozashtam ke va3 ye havaleyi ke anbar xodesh saader karde chand baar rush mayubi gozaresh nashe
defect = {
    ('d', 'defective'),
    ('n', 'not_defective')
}

#delivery status
deliveryChoices = (
    (0, u'صادر شده'),
    (1, u'در راه'),
    (2, u'دریافت شده')
)


# mowjudie anbar
class Stock(models.Model):
    product = models.ForeignKey(Product, verbose_name = u"کالا")
    quantity_returned = models.PositiveIntegerField(verbose_name = u"مقدار مرجوعی", default = 0)
    quantity = models.PositiveIntegerField(verbose_name = u"مقدار", default = 0)
    reserved_quantity = models.PositiveIntegerField(verbose_name = u'مقدار رزرو شده', default = 0)
    #in do ta bi estefade mund :-?
    rack_num_returned = models.IntegerField(verbose_name = u"شماره قفسه مرجوعی")
    rack_num = models.IntegerField(verbose_name = u"شماره قفسه")

    def enough_stock(self, number):
        if (self.quantity - self.reserved_quantity) > number:
            return True
        else:
            return False

# reside tahvile kala be anbaar
class Receipt_Delivery(models.Model):
    wiki = models.ForeignKey(Wiki, verbose_name = u"ویکی")
    product = models.ForeignKey(Product, verbose_name = u"کالا")
    quantity = models.IntegerField(verbose_name = u"مقدار")
    date = models.DateField(auto_now_add = True, verbose_name = u"تاریخ")

# havaleye tolid shode tavasote xode anbaar baraye ersaale mojadade kalahaaye mayoub
class Transference(models.Model):
    date = models.DateField(auto_now_add = True, verbose_name = u"تاریخ")
    product = models.ForeignKey(Product, verbose_name = u"کالا")
    bill = models.ForeignKey(SaleBill, verbose_name = u"فاکتور فروش")
    quantity = models.PositiveIntegerField(verbose_name = u"مقدار", default = 0)
    defective = models.CharField(max_length = 1, choices = defect, default = 'n')

# anvaae havalehaaye anbaar
class Clearance(models.Model):
    type = models.CharField(max_length = 9, choices = clear_type, verbose_name = u" مرجع حواله")
    date = models.DateField(verbose_name = u"تاریخ")
    bill = models.ForeignKey(SaleBill, verbose_name = u"فاکتور فروش", null = True, blank = True)
    wiki = models.ForeignKey(ReturnRequest, verbose_name = u"ویکی", null = True, blank = True)
    transfer = models.ForeignKey(Transference, verbose_name = u"حواله انبار", null = True, blank = True)
    ready = models.CharField(max_length = 1, choices = ready, default = 'n')

    # va3 inke admin ejaaze bede ke in field haro null sabt konam ino gozashtam
    def save(self, *args, **kwargs):
        if not self.bill:
            self.bill = None
        if not self.wiki:
            self.wiki = None
        if not self.transfer:
            self.transfer = None
        super(Clearance, self).save(*args, **kwargs)

# reside tarxise kalaa
class Receipt_Clearance(models.Model):
    date = models.DateField(auto_now_add = True, verbose_name = u"تاریخ")
    clearance = models.ForeignKey(Clearance, verbose_name = u"حواله")

# darxaste vorude kalaye jadid be wiki
class Wiki_Order(models.Model):
    date = models.DateField(auto_now_add = True, verbose_name = u"تاریخ")
    product = models.ForeignKey(Product, verbose_name = u"کالا")
    wiki = models.ForeignKey(Wiki, verbose_name = u"ویکی")
    quantity = models.PositiveIntegerField(verbose_name = u"مقدار")
    deliveryStatus = models.IntegerField(default = 0, choices = deliveryChoices, verbose_name = u'وضعیت تحویل')

# reside moshtari ya wiki
class Receipt_Customer_Wiki(models.Model):
    date = models.DateField(auto_now_add = True, verbose_name = u"تاریخ")
    clearance = models.ForeignKey(Clearance, verbose_name = u"حواله")
