from celery import shared_task


@shared_task(name='send_sms')
def send_sms(phone, text):
    from ..utils.sms import send_message
    send_message(phone, text)
    return 'OK'
