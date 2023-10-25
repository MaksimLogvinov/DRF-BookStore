from gettext import gettext

from celery import shared_task

from apps.main.services import send_message


@shared_task
def change_password_task(user):
    send_message(
        user=user,
        url_name='/user/reset-password',
        subject=gettext('Ваш пароль пытаются сменить'),
        message=gettext('Перейдите по следующей ссылке, '
                        'чтобы сменить пароль:')
    )
    return True


@shared_task
def verify_email_task(user):
    send_message(
        user=user,
        url_name='/user/confirm-email',
        subject=gettext('Подтвердите свой электронный адрес'),
        message=gettext('Пожалуйста, перейдите по следующей ссылке, '
                        'чтобы подтвердить свой адрес электронный'
                        ' почты:'))
    return True
