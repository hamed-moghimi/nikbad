# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import password_reset, password_reset_done

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy

admin.autodiscover()

urlpatterns = patterns('',
                       # index url
                       url(r'^$', 'sales.views.index', name = 'index'),
                       url(r'^login$', 'contrib.views.login', name = 'login'),
                       url(r'^logout', 'contrib.views.logout', name = 'logout'),
                       url(r'^bank$', 'contrib.views.bank', name = 'contrib-bank'),

                       # subsystem urls
                       url(r'^sales/', include('sales.urls')),
                       url(r'^wiki/', include('wiki.urls')),
                       url(r'^crm/', include('crm.urls')),
                       url(r'^warehouse/', include('warehouse.urls')),
                       url(r'^fnc/', include('fnc.urls')),
                       url(r'^mng/', include('mng.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)  # for serving media files


# urls for managing passwords
urlpatterns += patterns('django.contrib.auth.views',
                        url(r'^password_reset/$', 'password_reset',
                            {
                                'post_reset_redirect': reverse_lazy('forget_password_done'),
                                'template_name': 'contrib/simple.html',
                                # 'email_template_name': 'contrib/password_reset_email.html',
                                'extra_context':
                                    {
                                        'header': u'فراموشی رمز عبور',
                                        'prompt': u'رمز عبور خود را فراموش کرده اید؟ ایمیل خود را وارد کنید تا دستورالعمل لازم برای شما ارسال گردد.',
                                        'form_submit_text': u'ارسال درخواست',
                                    }
                            },
                            name = 'forget-password'),

                        url(r'^password_reset/done/$', 'password_reset_done',
                            {
                                'template_name': 'contrib/simple.html',
                                'extra_context':
                                    {
                                        'header': u'فراموشی رمز عبور',
                                        'message_success': u'ایمیل حاوی دستورالعمل لازم برای تغییر رمز عبور برای شما ارسال شد.',
                                    }
                            },
                            name = 'forget_password_done'),

                        url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm',
                            {
                                'template_name': 'contrib/simple.html',
                                'post_reset_redirect': reverse_lazy('reset_password_done'),
                                'extra_context':
                                    {
                                        'header': u'تغییر رمز عبور',
                                        'prompt': u'رمز عبور خود را تغییر دهید.',
                                        'error_message': u'کد وارد شده نادرست است یا قبلا استفاده شده است.',
                                        'submit_text': u'تغییر رمز عبور'
                                    }
                            }),

                        url(r'^reset/done/$', 'password_reset_complete',
                            {
                                'template_name': 'contrib/simple.html',
                                'extra_context':
                                    {
                                        'header': u'تغییر رمز عبور',
                                        'message_success': u'رمز عبور شما با موفقیت تغییر کرد. لطفا دوباره وارد شوید.',
                                    }
                            },
                            name = 'reset_password_done'),
)