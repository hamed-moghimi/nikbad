from django.core.exceptions import ValidationError


def clean_password(data):
    if isinstance(data, str) and len(data) >= 6:
        return data
    raise ValidationError(u'نام کاربری باید حداقل 6 حرف باشد.')