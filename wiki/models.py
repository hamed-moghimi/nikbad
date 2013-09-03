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
    phone = models.CharField("شماره تلفن", max_length = 12)
    address = models.CharField("نشانی", max_length = 1000)
    image = models.ImageField("تصویر نشان تجاری", blank = True, upload_to = 'images/wikis')
    reminder = models.IntegerField(verbose_name = "باقی مانده حقوق", default = 0)

    class Meta:
        verbose_name = u'ویکی'
        verbose_name_plural = u'ویکی ها'

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

class Brand(models.Model):
    name = models.CharField("نام تجاری", max_length=60)


    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'نام تجاری'
        verbose_name_plural = u'نام های تجاری'

class Product(models.Model):
    goodsID = models.IntegerField("کد کالا", primary_key = True)
    wiki = models.ForeignKey(Wiki, verbose_name = "نام ویکی")
    brand = models.ForeignKey(Brand, verbose_name="نام تجاری")
    name = models.CharField("نام کالا", max_length = 255)
    sub_category = models.ForeignKey(SubCat, verbose_name = "زیر دسته", on_delete=models.PROTECT)
    unit = models.CharField("واحد شمارش", default = "عدد", max_length = 30)
    price = models.IntegerField("قیمت", help_text = "قیمت را به ریال وارد نمایید")
    off = models.PositiveSmallIntegerField("تخفیف", default=0,
                                           help_text = "تخفیف یک عدد مثبت کوچکتر از 100 است")
    deliveryStatus = models.IntegerField(default = 0, choices = deliveryChoices, verbose_name = u'وضعیت تحویل')
    orderPoint = models.PositiveIntegerField(default = 0, verbose_name = u'نقطه سفارش')


    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'کالا'
        verbose_name_plural = u'کالاها'

    def raw_price(self):
        return self.price / (1 - self.off / 100.0)

    def isInSale(self):
        return self.off > 0


class Contract(models.Model):
    wiki = models.OneToOneField(Wiki, verbose_name = " نام ویکی")
    startDate = models.DateField("تاریخ شروع")
    expDate = models.DateField("تاریخ پایان")
    max_goods = models.IntegerField("حداکثر تعداد کالاهای ویترین")
    percent = models.PositiveSmallIntegerField("درصد بهره ی سراب از فروش")
    fee = models.PositiveIntegerField("آبونمان")

    def __unicode__(self):
        return self.wiki

    class Meta:
        verbose_name = u'قرارداد'
        verbose_name_plural = u'قراردادها'


class ReturnRequest(models.Model):
    wiki = models.ForeignKey(Wiki, verbose_name = u'نام ویکی')
    product = models.ForeignKey(Product, verbose_name = u'نام کالا')
    pub_date = models.DateField("تاریخ درخواست")
    deliveryStatus = models.IntegerField(default = 0, choices = deliveryChoices, verbose_name = u'وضعیت تحویل')
    returned_only = models.NullBooleanField(verbose_name = u'فقط کالاهای مرجوعی را بازگردان.')

    class Meta:
        verbose_name = u'درخواست بازگشت کالا از انبار'
        verbose_name_plural = u'درخواست های بازگشت کالا از انبار'



class ConRequest(models.Model):
    wiki = models.ForeignKey(Wiki, verbose_name = u'نام ویکی')
    pub_date = models.DateField("تاریخ ثبت درخواست ایجاد قرارداد")
    benefit = models.PositiveSmallIntegerField("کارمزد پیشنهادی برای سراب")
    abonne = models.PositiveIntegerField("آبونمان پیشنهادی برای هر ماه",
                                         help_text = "آبونمان پیشنهادی تان را به ریال وارد نمایید.")

    class Meta:
        verbose_name = u'درخواست ثبت قرارداد با ویکی'
        verbose_name_plural = u'درخواست های ثبت قرارداد با ویکی'


class ConCancel(models.Model):
    wiki = models.ForeignKey(Wiki, verbose_name = u'نام ویکی')
    pub_date = models.DateField("تاریخ ثبت درخواست لغو قرارداد")

    class Meta:
        verbose_name = u'درخواست لغو قرارداد با ویکی'
        verbose_name_plural = u'درخواست های لغو قرارداد با ویکی'
