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
    companyName = models.CharField("نام شرکت", max_length = 255)
    phone = models.SlugField("شماره تلفن", max_length = 11)
    address = models.CharField("نشانی", max_length = 1000)
    image = models.ImageField("تصویر نشان تجاری", blank = True, upload_to = 'images/wikis')
    reminder = models.IntegerField(verbose_name = "باقی مانده حقوق", default = 0)

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
    unit = models.CharField(verbose_name = u'واحد شمارش', default=u'عدد', max_length = 50)

    class Meta:
        verbose_name = u'نوع کالا'
        verbose_name_plural = u'انواع کالا'

    def __unicode__(self):
        return u'{0} ({1})'.format(self.name, self.category.name)


class Product(models.Model):
    goodsID = models.IntegerField("کد کالا", primary_key = True)
    wiki = models.ForeignKey(Wiki, verbose_name = "نام ویکی")
    brand = models.CharField("نام تجاری", max_length = 255)
    name = models.CharField("نام کالا", max_length = 255)
    sub_category = models.ForeignKey(SubCat, verbose_name = "زیر دسته")
    price = models.IntegerField("قیمت")
    off = models.PositiveSmallIntegerField("تخفیف", blank = True, null = True)
    deliveryStatus = models.IntegerField(default = 0, choices = deliveryChoices, verbose_name = u'وضعیت تحویل')


    def __unicode__(self):
        return self.name

    def finalPrice(self):
        return self.price * (100 - self.off) // 100

    def isInSale(self):
        return self.off != 0


class Contract(models.Model):
    wiki = models.OneToOneField(Wiki, verbose_name = " نام ویکی")
    startDate = models.DateField("تاریخ شروع")
    expDate = models.DateField("تاریخ پایان")
    max_goods = models.IntegerField("حداکثر تعداد کالاهای ویترین")
    percent = models.PositiveSmallIntegerField("درصد بهره ی سراب از فروش")
    fee = models.PositiveIntegerField("آبونمان")


class ReturnRequest(models.Model):
    wiki = models.ForeignKey(Wiki, verbose_name = u'نام ویکی')
    product = models.ForeignKey(Product, verbose_name = u'نام کالا')
    pub_date = models.DateField("تاریخ درخواست")
    deliveryStatus = models.IntegerField(default = 0, choices = deliveryChoices, verbose_name = u'وضعیت تحویل')
    returned_only = models.NullBooleanField(verbose_name = u'فقط کالاهای مرجوعی را بازگردان.')

class ConRequest(models.Model):
    wiki = models.ForeignKey(Wiki, verbose_name = u'نام ویکی')
    pub_date = models.DateField("تاریخ ثبت درخواست ایجاد قرارداد")
    benefit = models.PositiveSmallIntegerField("کارمزد پیشنهادی برای سراب")
    abonne = models.PositiveIntegerField("آبونمان پیشنهادی برای هر ماه")

    class Meta:
        verbose_name = u'درخواست ثبت قرارداد با ویکی'
        verbose_name_plural = u'درخواست های ثبت قرارداد با ویکی'

class ConCancel(models.Model):
    wiki = models.ForeignKey(Wiki, verbose_name = u'نام ویکی')
    pub_date = models.DateField("تاریخ ثبت درخواست لغو قرارداد")

    class Meta:
        verbose_name = u'درخواست لغو قرارداد با ویکی'
        verbose_name_plural = u'درخواست های لغو قرارداد با ویکی'
