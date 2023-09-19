import logging
import os

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext


def send_message(user, url_name, subject, message):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_url = reverse_lazy(
        url_name,
        kwargs={'uidb64': uid, 'token': token}
    )
    current_site = Site.objects.get_current().domain
    if current_site == 'example.com':
        current_site = os.environ.get('LOCALE_URL')
    send_mail(subject=subject,
              message=message + f'http://{current_site}{activation_url}',
              recipient_list=[user.email],
              from_email=os.environ.get('EMAIL_HOST_USER'),
              fail_silently=False)
    logging.log(51, gettext("Сообщение отправлено"))


def send_email(recipient, link, subject, message):
    current_site = Site.objects.get_current().domain
    if current_site == 'example.com':
        current_site = os.environ.get('LOCALE_URL')
    send_mail(subject=subject,
              message=message + f"http://{current_site}/" + link,
              recipient_list=[recipient],
              from_email=os.environ.get('EMAIL_HOST_USER'),
              fail_silently=False)
