from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from email.mime.multipart import MIMEMultipart
from mail.base import mail
from preferences.utils import get_setting


@shared_task(name='send_mail')
def send_mail(name, to_email, subject, context, to_name=''):

    mail(name, to_email, subject, context, to_name)
    return 'OK'


# @shared_task(name='send_mail_html')
def send_mail_html(name, to_email, subject, context):

    from_email = '%s <%s>' % (get_setting('mail_sendername', ''), get_setting('mail_sendermail', ''))

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    context['page_url'] = get_setting('website_siteurl', '')
    context['site_url'] = get_setting('website_siteurl', '')
    context['site_name'] = get_setting('website_sitename', '')

    text_content = render_to_string('mail/%s.txt' % name, context)
    html_content = render_to_string('mail/%s.html' % name, context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return 'OK'
