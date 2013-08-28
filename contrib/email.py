from django.core.mail import EmailMultiAlternatives
from django.template.base import Template
from django.template.loader import get_template
from django.template import Context


def render_and_email(to_list, subject, text_template = None, html_template = None, context_dic = None):
    '''
    This method gets a list of recipients, a subject text, text_template (for showing in web readers and mobile apps),
    an HTML_template for displaying in browsers and a context dictionary, renders templates with context
    and sends an email.
    Note that if text_template is a filename, method loads it, otherwise uses it as string (And same for html_template).
    '''

    from_email = 'no-reply@nikbad.ir'
    context = Context(context_dic)

    if text_template:
        try:
            plaintext = get_template(text_template)
        except:
            plaintext = Template(text_template)
        text_content = plaintext.render(context)
    else:
        text_content = '(EMPTY)'

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_list)

    if html_template:
        try:
            htmly = get_template(html_template)
        except:
            htmly = Template(html_template)
        html_content = htmly.render(context)
        msg.attach_alternative(html_content, "text/html")

    msg.send()