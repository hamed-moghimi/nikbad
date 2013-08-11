# -*- coding: utf-8 -*-
from django.contrib.humanize.templatetags.humanize import intcomma
from django import template
register = template.Library()

@register.filter
def rial(currency):
    return u'{0} ریال'.format(intcomma(int(currency), False))

@register.filter
def toman(currency):
    return u'{0} تومان'.format(intcomma(int(int(currency) / 10), False))