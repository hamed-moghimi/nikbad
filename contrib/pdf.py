# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pyPdf import PdfFileWriter, PdfFileReader
from StringIO import StringIO
import unicodedata
from bidi.algorithm import get_display
from arabic_rtlize import process as a_process
from arabic_rtlize import forms as a_forms
from django.conf import settings
import os.path

# initialize fonts
pdfmetrics.registerFont(TTFont('Nazanin', file(os.path.join(settings.ROOT_DIR, 'static/fonts/BNazanin.ttf'), 'rb')))
pdfmetrics.registerFont(TTFont('Arial', file(os.path.join(settings.ROOT_DIR, 'static/fonts/arial.ttf'), 'rb')))


def drawText(canvas, x, y, text, en = False):
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
    if en:
        canvas.setFont('Arial', 8)
    else:
        canvas.setFont('Nazanin', 12)
    canvas.drawRightString(x, y, wrkText)


class BulletMark():
    def __init__(self, x, y):
        self.x, self.y, self.text = x, y, u'*'

    def draw(self, canvas):
        drawText(canvas, self.x, self.y, self.text)


class StringMark():
    def __init__(self, x, y, text, en = False):
        self.x, self.y, self.text, self.en = x, y, unicode(text), en
        if self.text.lower() == 'none':
            self.text = u'----'

    def draw(self, canvas):
        drawText(canvas, self.x, self.y, self.text, self.en)


class PDFWriter():
    def __init__(self, original_file):

        self.original_file = original_file
        self.original_pdf = PdfFileReader(self.original_file)

        self.buffer = StringIO()
        self.canvas = canvas.Canvas(self.buffer)
        self.canvas.setFillColorRGB(0, 0, 1)

        self.outputstream = StringIO()
        self.output = PdfFileWriter()


    def save(self):
        self.canvas.save()
        self.watermark = PdfFileReader(self.buffer)
        return self.canvas


    def draw(self, items):
        for item in items:
            item.draw(self.canvas)


    def merge(self):
        ix = 0
        for page in self.original_pdf.pages:
            if self.watermark.numPages >= ix + 1:
                page.mergePage(self.watermark.getPage(ix))
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
def getPDF_Response(base_filename, texts):
    with file(base_filename, 'rb') as base_file:
        p = PDFWriter(base_file)
        p.draw(texts)
        pdf = p.export()
        response = HttpResponse(mimetype = 'application/pdf')
        #response['Content-Disposition'] = 'attachment; filename=report.pdf'
        response.write(pdf)
        return response