# -*- encoding: utf-8 -*-
from re import match
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pyPdf import PdfFileWriter, PdfFileReader
from StringIO import StringIO
import unicodedata
from bidi.algorithm import get_display
from reportlab.pdfgen.canvas import Canvas
from arabic_rtlize import process as a_process
from arabic_rtlize import forms as a_forms
from django.conf import settings
import os.path

# initialize fonts
pdfmetrics.registerFont(TTFont('Nazanin', file(os.path.join(settings.ROOT_DIR, 'static/fonts/BNazanin.ttf'), 'rb')))
pdfmetrics.registerFont(
    TTFont('BNazanin', file(os.path.join(settings.ROOT_DIR, 'static/fonts/BNazaninBold.ttf'), 'rb')))


def drawText(canvas, x, y, text, en = False, bold = False):
    wrkText = text
    isArabic = False
    isBidi = False
    for c in wrkText:
        cat = unicodedata.bidirectional(c)
        if cat == "AL" or cat == "AN" or cat == "FA":
            isArabic = True
            isBidi = True
            break
        elif cat == "R" or cat == "RLE" or cat == "RLO":
            isBidi = True
    if isArabic:
        wrkText = a_forms.fuse(wrkText)
        wrkText = a_process.shape(wrkText)

    if isBidi:
        wrkText = get_display(wrkText)

    if bold:
        canvas.setFont('BNazanin', 12)
    else:
        canvas.setFont('Nazanin', 12)

    canvas.drawRightString(x, canvas._pagesize[1] - y, wrkText)


class BulletMark():
    def __init__(self, x, y):
        self.x, self.y, self.text = x, y, u'*'

    def draw(self, canvas):
        drawText(canvas, self.x, self.y, self.text)


ord0 = ord(u'0')
ord9 = ord(u'9')


class StringMark():
    def __init__(self, x, y, text, en = False, bold = False, auto_number = True):
        self.x, self.y, self.text, self.en, self.bold = x, y, unicode(text), en, bold
        if self.text.lower() == 'none':
            self.text = ''

        # replace digits with farsi digits
        if auto_number:
            newText = ''
            for c in self.text:
                newText += ord0 <= ord(c) <= ord9 and unichr(ord(c) + 1728) or c
            self.text = newText

    def draw(self, canvas):
        drawText(canvas, self.x, self.y, self.text, self.en, self.bold)


class PDFWriter():
    def __init__(self, original_file, pageSize):

        self.original_file = original_file

        self.buffer = StringIO()
        self.canvas = canvas.Canvas(self.buffer, pagesize = pageSize)

        self.output = PdfFileWriter()


    def save(self):
        self.canvas.save()
        self.watermark = PdfFileReader(self.buffer)
        return self.canvas


    def draw_page(self, items):
        self.canvas.setFillColorRGB(0, 0, 1)
        for item in items:
            item.draw(self.canvas)
        self.canvas.showPage()


    def merge(self):
        self.original_pdf = PdfFileReader(self.original_file)
        ix = 0
        for page in self.original_pdf.pages:
            if self.watermark.numPages >= ix + 1:
                page.mergePage(self.watermark.getPage(ix))
                ix += 1
            self.output.addPage(page)

        return self.output


    def export(self):
        self.save()
        self.merge()
        io = StringIO()
        self.output.write(io)
        self.close()
        return io.getvalue()


    def close(self):
        self.buffer.close()


# codes by Hamed
def getPDF_Response(texts, base_filename, pageSize = A4, orientation = portrait):
    with open(base_filename, 'rb') as base_file:
        template = PdfFileReader(base_file)
        temp = StringIO()
        w = PdfFileWriter()
        p = template.pages[0]
        for i in texts:
            w.addPage(p)
        w.write(temp)

    p = PDFWriter(temp, pageSize = orientation(pageSize))

    for pageContent in texts:
        p.draw_page(pageContent)

    pdf = p.export()
    response = HttpResponse(mimetype = 'application/pdf')
    #response['Content-Disposition'] = 'attachment; filename=report.pdf'
    response.write(pdf)
    temp.close()
    return response