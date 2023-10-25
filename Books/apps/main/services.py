import logging
import os
from gettext import gettext

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_message(user, url_name, subject, message):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    send_mail(subject=subject,
              message=message + f'http://{os.environ.get("LOCALE_URL")}'
                                f'{url_name}/{uid}/{token}',
              recipient_list=[user.email],
              from_email=os.environ.get('EMAIL_HOST_USER'),
              fail_silently=False)
    logging.log(51, gettext('Сообщение отправлено'))


def send_email(recipient, link, subject, message):
    try:
        send_mail(
            subject=subject,
            message=message + f"http://{os.environ.get('LOCALE_URL')}/" + link,
            recipient_list=[recipient],
            from_email=os.environ.get('EMAIL_HOST_USER'),
            fail_silently=False
        )
    except Exception:
        return logging.log(51, 'Смс попало в спам')