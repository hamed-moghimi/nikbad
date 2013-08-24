# -*- encoding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

# from django.test import TestCase
#
#
# class SimpleTest(TestCase):
#     def test_basic_addition(self):
#         """
#         Tests that 1 + 1 always equals 2.
#         """
#         self.assertEqual(1 + 1, 2)

# from StringIO import StringIO
from django.http import HttpResponse
from contrib.pdf import getPDF_Response
from pdf import PDFWriter, StringMark


def test(request):
    a = [
        StringMark(470, 290, u'سید حامد'),
        StringMark(430, 260, u'مقیمی'),
    ]
    return getPDF_Response(r'C:\Users\Hamed\Desktop\a.pdf', a)