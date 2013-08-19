# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.forms.models import ModelForm


class ForgetPasswordForm(ModelForm):
    def clean_username(self):
        return self.data['username']

    def clean(self):
        cleaned_data = super(ForgetPasswordForm, self).clean()
        if 'username' in cleaned_data and 'email' in cleaned_data:
            if not User.objects.exists(username = cleaned_data['username'], email = self.cleaned_data['email']):
                del cleaned_data['username']
                del cleaned_data['email']
                self._errors['username'] = self.error_class(u'کاربری با این مشخصات یافت نشد')
            else:
                self.user = User.objects.get(username = cleaned_data['username'], email = self.cleaned_data['email'])

        return cleaned_data

    class Meta:
        model = User
        fields = ['username', 'email']