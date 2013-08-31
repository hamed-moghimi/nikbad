# -*- encoding: utf-8 -*-
from django.db import models
from django.db.models.expressions import F
from wiki.models import Product
from crm.models import Customer

deliveryChoices = (
    (0, u'صادر شده'),
    (1, u'در راه'),
    (2, u'دریافت شده')
)
from django.db.models.fields import *

# Create your models here.
class SaleBill(models.Model):
    # general fields
    saleDate = models.DateField(auto_now_add = True, verbose_name = u'تاریخ فروش')
    totalPrice = models.IntegerField(default = 0, verbose_name = u'مبلغ کل')
    customer = models.ForeignKey(Customer, related_name = 'saleBills', verbose_name = u'خریدار')

    # transportation fields
    deliveryStatus = models.IntegerField(default = 0, choices = deliveryChoices, verbose_name = u'وضعیت تحویل')

    # relation with products
    productList = models.ManyToManyField(Product, through = 'SaleBill_Product')

    class Meta:
        verbose_name = u'فاکتور فروش'
        verbose_name_plural = u'فاکتورهای فروش'
        ordering = ['-saleDate', 'deliveryStatus', 'customer']

    @staticmethod
    def createFromMarketBasket(basket):
        sb = SaleBill()
        sb.customer = basket.customer
        sb.totalPrice = basket.totalPrice
        sb.save()

        products = [SaleBill_Product(bill = sb, product = i.product, number = i.number) for i in basket.items.all()]
        sb.products.bulk_create(products)

        # updating popularity
        q = Ad.objects.filter(product__in = basket.items.values('product')).update(popularity = F('popularity') + 1)

        return sb


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
    customer = models.OneToOneField(Customer, related_name = 'marketBasket', verbose_name = u'خریدار')

    # relation with products
    productList = models.ManyToManyField(Product, through = 'MarketBasket_Product')

    class Meta:
        verbose_name = u'سبد خرید'
        verbose_name_plural = u'سبدهای خرید'

    # variables
    itemsNum = 0  # should update every time an item removed or added or object created

    def __init__(self, *args, **kwargs):
        super(MarketBasket, self).__init__(*args, **kwargs)
        self.itemsNum = self.items.count()
        print(self.itemsNum)

    def __unicode__(self):
        return u'سبد خرید ({0} مورد)'.format(self.itemsNum)

    @staticmethod
    def createForCustomer(customer):
        MarketBasket.objects.get_or_create(customer = customer)

    def add_item(self, product):
        if self.set_item(product, -1):
            self.itemsNum += 1
            return True
        return False

    def set_item(self, product, number):
        (item, created) = self.items.get_or_create(product = product)
        if number != -1:
            item.number = number
        item.save()
        self.calculateTotalPrice()
        return created

    def remove_item(self, product):
        item = self.items.filter(product = product)
        if item.exists():
            self.itemsNum -= 1
            item.delete()
            self.calculateTotalPrice()
            return True
        return False

    def updateItems(self):
        self.itemsNum = self.items.count()
        self.calculateTotalPrice()

    def calculateTotalPrice(self):
        p = 0
        for item in self.items.all():
            p += item.product.price * item.number
        self.totalPrice = p
        self.save()

    def clear(self):
        self.totalPrice = 0
        self.items.all().delete()
        self.save()
        self.itemsNum = 0


class MarketBasket_Product(models.Model):
    # foreign keys
    basket = models.ForeignKey(MarketBasket, related_name = 'items')
    product = models.ForeignKey(Product, related_name = 'baskets')

    # fields
    number = models.IntegerField(default = 1)


class Ad(models.Model):
    product = models.OneToOneField(Product)
    description = models.TextField(verbose_name = u'توضیحات', blank = True)
    registerDate = models.DateField(auto_now_add = True, verbose_name = u'تاریخ ثبت')
    popularity = models.IntegerField(default = 0, verbose_name = u'محبوبیت')

    def _get_self_id(self):
        return self.id

    icon = models.ForeignKey('AdImage', related_name = 'belongs', null = True, blank = True)

    class Meta:
        verbose_name = u'ویترین'
        verbose_name_plural = u'ویترین ها'
        ordering = ['-registerDate']

    def __unicode__(self):
        return self.product.__unicode__()

    @staticmethod
    def defaultIcon():
        from nikbad import settings

        return settings.STATIC_URL + 'sales/images/default.png'

    @staticmethod
    def createForProduct(product):
        Ad.objects.get_or_create(product = product)

    def addMarketButton(self):
        try:
            return self.product.stock_set.all()[0].enough_stock(0)
        except:
            return False


class Specification(models.Model):
    ad = models.ForeignKey(Ad, related_name = 'specs')
    title = models.CharField(max_length = 30, verbose_name = u'عنوان', blank = True)
    value = models.CharField(max_length = 100, verbose_name = u'محتوا')

    class Meta:
        verbose_name = u'ویژگی'
        verbose_name_plural = u'ویژگی ها'
        ordering = ['ad', '-title']

    def __unicode__(self):
        return u'{0} - {1}'.format(self.title, self.value)


# function for generating image path
def image_path(instance, filename):
    return 'images/vitrin/{0}/{1}'.format(instance.ad.id, filename)


class AdImage(models.Model):
    ad = models.ForeignKey(Ad, related_name = 'images', blank = True)
    title = models.CharField(max_length = 30, verbose_name = u'عنوان')
    image = models.ImageField(upload_to = image_path, verbose_name = u'تصویر')

    class Meta:
        verbose_name = u'تصویر'
        verbose_name_plural = u'تصاویر'
        ordering = ['ad', 'title']

    def __unicode__(self):
        return u'{0} - {1}'.format(self.ad.__unicode__(), self.title)

    def thumbnail(self):
        return '<img src={0} style="width: 30px; height: 30px" />'.format(self.image.url)

    thumbnail.allow_tags = True
    thumbnail.short_description = u'تصویر'