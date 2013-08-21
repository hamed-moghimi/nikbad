# -*- encoding: utf-8 -*-
import datetime
from django import forms
from django.forms.util import flatatt
from django.utils.encoding import force_unicode
from django.utils.formats import get_format
from django.utils.safestring import mark_safe

calbtn = u'''<img src="/static/contrib/css/jscalendar/skins/cal.png" alt="calendar" id="%s_btn"
style="cursor: pointer; width: 18px; height:18px; vertical-align:middle; float: none;" title="انتخاب تاریخ" />
<script type="text/javascript">
    function onJalaliDateSelected(calendar, date) {
        var e = document.getElementById("%s");
        var str = calendar.date.getFullYear() + "-" + (calendar.date.getMonth() + 1) + "-" + calendar.date.getDate();
        e.value = str;
    }
    Calendar.setup({
        inputField     :    "%s_display",   
        button         :    "%s_btn",
        ifFormat       :    "%s",
        dateType       :    "jalali",
        weekNumbers    :     false,
        onUpdate       :     onJalaliDateSelected
    });
</script>'''


class DateTimeWidget(forms.widgets.TextInput):
    class Media:
        css = {
            'all': ('/static/contrib/css/jscalendar/skins/calendar-blue.css',)
        }
        js = (
            '/static/contrib/js/jscalendar/jalali.js',
            '/static/contrib/js/jscalendar/calendar.js',
            '/static/contrib/js/jscalendar/calendar-setup.js',
            '/static/contrib/js/jscalendar/lang/calendar-fa.js',
        )

    dformat = '%Y-%m-%d'

    def render(self, name, value, attrs = None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, type = self.input_type, name = name)
        if value != '':
            try:
                final_attrs['value'] = \
                    force_unicode(value.strftime(self.dformat))
            except:
                final_attrs['value'] = \
                    force_unicode(value)
        if not final_attrs.has_key('id'):
            final_attrs['id'] = u'%s_id' % (name)
        id = final_attrs['id']

        jsdformat = self.dformat #.replace('%', '%%')
        cal = calbtn % (id, id, id, id, jsdformat)
        parsed_atts = flatatt(final_attrs)
        a = u'<span><input type="text" id="%s_display" disabled = "disabled"/><input type="hidden" %s/> %s%s</span>' % (
            id, parsed_atts, self.media, cal)
        return mark_safe(a)

    def value_from_datadict(self, data, files, name):
        dtf = '%Y-%m-%d' #
        t = get_format('DATETIME_FORMAT') #forms.fields.DEFAULT_DATETIME_INPUT_FORMATS
        empty_values = forms.fields.EMPTY_VALUES

        value = data.get(name, None)
        if value in empty_values:
            return None
        if isinstance(value, datetime.datetime):
            return value
        if isinstance(value, datetime.date):
            return datetime.datetime(value.year, value.month, value.day)

        try:
            return datetime.datetime.strptime(value, dtf)
        except ValueError:
            return None

    def _has_changed(self, initial, data):
        """
        Return True if data differs from initial.
        Copy of parent's method, but modify value with strftime function before final comparsion
        """
        if data is None:
            data_value = u''
        else:
            data_value = data

        if initial is None:
            initial_value = u''
        else:
            initial_value = initial

        try:
            if force_unicode(initial_value.strftime(self.dformat)) != force_unicode(data_value.strftime(self.dformat)):
                return True
        except:
            if force_unicode(initial_value) != force_unicode(data_value):
                return True
        return False
