# -*- encoding: utf-8 -*-
from reportlab.lib.pagesizes import landscape, letter
from contrib.pdf import getPDF_Response, drawText
from pdf import PDFWriter, StringMark


def test(request):
    a = [
        [
            StringMark(300, 400, u'سلام Salam'),
            StringMark(300, 200, u'Salam'),
        ],

        [
            StringMark(470, 290, u'سید حامد'),
            StringMark(430, 260, u'مقیمی'),
        ],
    ]
    return getPDF_Response(a, r'C:\Users\Hamed\Desktop\a.pdf', pageSize = letter,
                           orientation = landscape) #r'C:\Users\Hamed\Desktop\a.pdf'