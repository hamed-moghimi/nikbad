# -*- encoding: utf-8 -*-
from django.db import models
from wiki.models import Product
from crm.models import Customer

deliveryChoices = (
    (0, u'صادر شده'),
    (1, u'در راه'),
    (2, u'دریافت شده')
)


# Create your models here.
class SaleBill(models.Model):
    # general fields
    saleDate = models.DateField(auto_now_add = True, verbose_name = u'تاریخ فروش')
    totalPrice = models.IntegerField(default = 0, verbose_name = u'مبلغ کل')
    costumer = models.ForeignKey(Customer, related_name = 'saleBills', verbose_name = u'خریدار')

    # transportation fields
    deliveryStatus = models.IntegerField(default = 0, choices = deliveryChoices, verbose_name = u'وضعیت تحویل')

    # relation with products
    productList = models.ManyToManyField(Product, through = 'SaleBill_Product')

    class Meta:
        verbose_name = u'فاکتور فروش'
        verbose_name_plural = u'فاکتورهای فروش'
        ordering = ['-saleDate', 'deliveryStatus', 'costumer']


class SaleBill_Product(models.Model):
    # foreign keys
    bill = models.ForeignKey(SaleBill, related_name = 'products')
    product = models.ForeignKey(Product, related_name = 'saleBills')

    # fields
    number = models.IntegerField(default = 1)


class MarketBasket(models.Model):
    # general fields
    lastModified = models.DateTimeField(auto_now = True, verbose_name = u'آخرین تغییر')
    totalPrice = models.IntegerField(default = 0, verbose_name = u'مبلغ کل')
    costumer = models.OneToOneField(Customer, related_name = 'marketBasket', verbose_name = u'خریدار')

    # relation with products
    productList = models.ManyToManyField(Product, through = 'MarketBasket_Product')

    # variables
    itemsNum = 0  # should update every time an item removed or added

    class Meta:
        verbose_name = u'سبد خرید'
        verbose_name_plural = u'سبدهای خرید'

    def __unicode__(self):
        return u'سبد خرید ({0} مورد)'.format(self.itemsNum)

    def add_item(self, product):
        if self.set_item(product, 1):
            self.itemsNum += 1
            return True
        return False

    def set_item(self, product, number):
        (item, created) = self.items.get_or_create(product = product)
        item.number = number
        item.save()
        return created

    def remove_item(self, product):
        item = self.items.filter(product = product)
        if item.exists():
            self.itemsNum -= 1
            item.delete()
            return True
        return False


class MarketBasket_Product(models.Model):
    # foreign keys
    basket = models.ForeignKey(MarketBasket, related_name = 'items')
    product = models.ForeignKey(Product, related_name = 'baskets')

    # fields
    number = models.IntegerField(default = 0)


class Ad(models.Model):
    product = models.OneToOneField(Product)
    description = models.TextField(verbose_name = u'توضیحات')

    class Meta:
        verbose_name = u'ویترین'
        verbose_name_plural = u'ویترین ها'

    def __unicode__(self):
        return self.product.__unicode__()


class Specification(models.Model):
    ad = models.ForeignKey(Ad, related_name = 'specs')
    title = models.CharField(max_length = 30, verbose_name = u'عنوان', blank = True)
    value = models.CharField(max_length = 100, verbose_name = u'محتوا')

    class Meta:
        verbose_name = u'ویژگی'
        verbose_name = u'ویژگی ها'
        ordering = ['ad', 'title']

    def __unicode__(self):
        return u'{0} - {1}'.format(self.title, self.value)


# function for generating image path
def image_path(instance, filename):
    return 'ad_images/{0}'.format(instance.ad.id)


class AdImage(models.Model):
    ad = models.ForeignKey(Ad, related_name = 'images')
    title = models.CharField(max_length = 30, verbose_name = u'عنوان')
    image = models.ImageField(upload_to = image_path, verbose_name = u'تصویر')

    class Meta:
        verbose_name = u'تصویر'
        verbose_name = u'تصاویر'
        ordering = ['ad', 'title']

    def __unicode__(self):
        return self.ad.id