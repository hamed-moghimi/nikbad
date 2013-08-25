from django.forms.fields import DateField, DateTimeField
from contrib.jalali_widget import DateTimeWidget


class jDateField(DateField):
    widget = DateTimeWidget()


class jDateTimeField(DateTimeField):
    widget = DateTimeWidget()


from django.forms.widgets import TextInput


class NumberInput(TextInput):
    input_type = 'number'