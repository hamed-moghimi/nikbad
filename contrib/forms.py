from django.forms.fields import DateField, DateTimeField
from contrib.jalali_widget import DateTimeWidget
from django.forms.widgets import TextInput


class jDateField(DateField):
    widget = DateTimeWidget()


class jDateTimeField(DateTimeField):
    widget = DateTimeWidget()


class NumberInput(TextInput):
    input_type = 'number'