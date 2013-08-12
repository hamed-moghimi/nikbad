# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


deliveryChoices = (
    (0, u'صادر شده'),
    (1, u'در راه'),
    (2, u'دریافت شده')
)


# Create your models here.
class Wiki(User):
    companyName = models.CharField("نام شرکت", max_length=255)
    description = models.TextField("شرح کالا و خدمات", blank=True, null=True)
    phone = models.SlugField("شماره تلفن")
    address = models.CharField("نشانی", max_length=1000)
    image = models.ImageField("تصویر لوگو", blank=True, upload_to='images/wikis')

    def __unicode__(self):
        return self.companyName


class Category(models.Model):
    name = models.CharField(max_length = 50, verbose_name = u'عنوان')

    class Meta:
        verbose_name = u'دسته بندی کالا'
        verbose_name_plural = u'دسته بندی های کالا'

    def __unicode__(self):
        return self.name


class SubCat(models.Model):
    name = models.CharField(max_length = 50, verbose_name = u'عنوان')
    # Some other properties here, hazineye anbardari and ... :D
    category = models.ForeignKey('Category', verbose_name = u'دسته', related_name = 'subCats')

    class Meta:
        verbose_name = u'نوع کالا'
        verbose_name_plural = u'انواع کالا'

    def __unicode__(self):
        return u'{0} ({1})'.format(self.name, self.category.name)


class Product(models.Model):
    goodsID = models.IntegerField("کد کالا", primary_key=True)
    wiki = models.ForeignKey(Wiki, verbose_name="کد ویکی")
    brand = models.CharField("برند", max_length=255)
    name = models.CharField("نام کالا", max_length=255)
    sub_category = models.ForeignKey(SubCat, verbose_name = "زیر دسته")
    price = models.IntegerField("قیمت")
    off = models.PositiveSmallIntegerField("تخفیف", blank=True, null=True)
    volume = models.PositiveIntegerField("حجم", default=0)
    unit = models.CharField(default=u'عدد', verbose_name=u'واحد شمارش', max_length=100)
    deliveryStatus = models.IntegerField(default = 0, choices = deliveryChoices, verbose_name = u'وضعیت تحویل')


    def __unicode__(self):
        return self.name


class Contract(models.Model):
    wiki = models.OneToOneField(Wiki, verbose_name="کد ویکی")
    startDate = models.DateField("تاریخ شروع")
    expDate = models.DateField("تاریخ پایان")
    max_goods = models.IntegerField("حداکثر تعداد کالاهای ویترین")
    percent = models.PositiveSmallIntegerField("درصد تسهیم سود")
    fee = models.PositiveIntegerField("آبونمان")

class ReturnRequest(models.Model):
    wiki = models.ForeignKey(Wiki, verbose_name=u'کد ویکی')
    product = models.ForeignKey(Product, verbose_name=u'کد کالا')
    pub_date = models.DateField("تاریخ درخواست")
    deliveryStatus = models.IntegerField(default = 0, choices = deliveryChoices, verbose_name = u'وضعیت تحویل')
    returned_only = models.BooleanField(verbose_name=u'فقط کالاهای مرجوعی را بازگردان.')

