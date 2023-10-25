from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

from apps.users.tasks import verify_email_task


def register_user(serializer):
    if serializer.is_valid():
        user = serializer.save()
        verify_email_task(user)
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
