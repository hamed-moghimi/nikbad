# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.humanize.templatetags.humanize import intcomma
from django import template
import jdatetime

register = template.Library()


@register.filter
def rial(currency):
    return u'{0} ریال'.format(intcomma(int(currency), False))


@register.filter
def toman(currency):
    return u'{0} تومان'.format(intcomma(int(int(currency) / 10), False))


@register.filter
def jalali(dateTime):
    try:
        convert = jdatetime.GregorianToJalali(dateTime.year, dateTime.month, dateTime.day)
        year, month, day = convert.getJalaliList()
        if isinstance(dateTime, datetime):
            result = datetime(year = year + 1000, month = month, day = day, hour = dateTime.hour, minute = dateTime.minute,
                              second = dateTime.second)
            return result.strftime('%y/%m/%d - %H:%M')
        else:
            result = datetime(year = year + 1000, month = month, day = day)
            return result.strftime('%y/%m/%d')
    except:
        return ''