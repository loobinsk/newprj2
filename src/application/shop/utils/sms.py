import requests

from django.conf import settings


def send_message(phone, text):
    r = requests.post(
        'https://sms4b.ru/ws/sms.asmx/SendSMS',
        data={
            'Login': settings.SMS4B_LOGIN,
            'Password': settings.SMS4B_PASSWORD,
            'Source': settings.SMS4B_SOURCE,
            'Phone': phone,
            'Text': text
        }
    )
