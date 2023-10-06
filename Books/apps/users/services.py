import logging
import os

from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext


def register_user(serializer):
    if serializer.is_valid():
        user = serializer.save()
        send_message(
            user=user,
            url_name='/user/confirm-email',
            subject=gettext('Подтвердите свой электронный адрес'),
            message=gettext('Пожалуйста, перейдите по следующей ссылке, '
                            'чтобы подтвердить свой адрес электронный'
                            ' почты:'))
        data = {'response': True}
    else:
        data = {'errors': serializer.errors}
    return data


def check_user_with_token(uidb64, user):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = user.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    return user


def confirm_email(uidb64, token, user, request):
    user = check_user_with_token(uidb64, user)
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        data = {'result': 'Ваш электронный адрес успешно активирован'}
    else:
        data = {'result': 'Почта не была подтверждена'}
    return data


def check_access(uidb64, token, user):
    user = check_user_with_token(uidb64, user)
    if user is not None and default_token_generator.check_token(user, token):
        url = 'failed/'
    else:
        url = 'done/'
    return url


def change_password(serializer, request):
    if not serializer.is_valid():
        return {'result': 'Неправильно заполнены поля'}
    if serializer.data['new_password1'] == serializer.data['new_password2']:
        request.user.set_password(str(serializer.data['new_password1']))
        request.user.save()
    return {'result': 'Ваш пароль был успешно изменён'}


def profile_update(serializer, user):
    if serializer.is_valid():
        serializer.update(
            instance=user,
            validated_data=serializer.data
        )
        data = {'result': 'Данные успешно обновлены'}
    else:
        data = {'errors': serializer.errors}
    return data


def user_update(serializer, user_profile):
    if serializer.is_valid():
        serializer.update(
            validated_data=serializer.data,
            instance=user_profile
        )
        data = {'result': 'Вы успешно изменили данные'}
    else:
        data = {'errors': serializer.errors}
    return data


def send_message(user, url_name, subject, message):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = Site.objects.get_current().domain
    if current_site == 'example.com':
        current_site = os.environ.get('LOCALE_URL')
    send_mail(subject=subject,
              message=message + f'http://{current_site}{url_name}/{uid}/{token}',
              recipient_list=[user.email],
              from_email=os.environ.get('EMAIL_HOST_USER'),
              fail_silently=False)
    logging.log(51, gettext('Сообщение отправлено'))


def send_email(recipient, link, subject, message):
    current_site = Site.objects.get_current().domain
    if current_site == 'example.com':
        current_site = os.environ.get('LOCALE_URL')
    try:
        send_mail(
            subject=subject,
            message=message + f"http://{current_site}/" + link,
            recipient_list=[recipient],
            from_email=os.environ.get('EMAIL_HOST_USER'),
            fail_silently=False
        )
    except Exception:
        return logging.log(51, 'Смс попало в спам')
