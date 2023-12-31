import os
from gettext import gettext

from django.contrib.auth import get_user_model, login
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect
from django.utils.http import urlsafe_base64_decode
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import CustomUser
from apps.users.serializers import (
    UserRegisterSerializer, ChangePasswordSerializer, SaveUserSerializer,
    SaveProfileSerializer
)
from apps.users.services import send_message

User = get_user_model()


class RegisterUserViewSet(viewsets.ViewSet):
    serializer_class = UserRegisterSerializer
    queryset = CustomUser.objects.all()

    def list(self, request, *args, **kwargs):
        return Response()

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
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
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
        return Response(data)


class UserConfirmEmailView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return Response(
                data={'result': 'Ваш электронный адрес успешно активирован'}
            )
        else:
            return Response(
                data={'result': 'Почта не была подтверждена'}
            )


class ResetPasswordView(APIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response()

    def post(self, request):
        content = {'text': gettext('Запрос за сброс пароля отправлен')}
        send_message(
            user=self.request.user,
            url_name='/user/reset-password',
            subject=gettext('Ваш пароль пытаются сменить'),
            message=gettext('Перейдите по следующей ссылке, '
                            'чтобы сменить пароль:'))
        return Response(content, status=status.HTTP_200_OK)


class EmailResetPasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            url = 'failed/'
        else:
            url = 'done/'
        return HttpResponseRedirect(redirect_to=url)


class ResetPasswordDoneView(APIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, uidb64):
        return Response(data={'result': 'Смена пароля'})

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'result': 'Неправильно заполнены поля'})
        if serializer.data['new_password1'] == serializer.data['new_password2']:
            request.user.set_password(str(serializer.data['new_password1']))
            request.user.save()
        return Response(data={'result': 'Ваш пароль был успешно изменён'})


class ResetPasswordFailedView(APIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request, uidb64):
        return Response(data={'result': 'Ошибка сброса пароля'})


class ProfileUserViewSet(viewsets.ViewSet):
    serializer_class = SaveUserSerializer
    permission_classes = (IsAuthenticated, )
    queryset = CustomUser.objects.all()

    def list(self, request, *args, **kwargs):
        return Response(data={'result': 'Информация о пользователе'})

    def post(self, request, *args, **kwargs):
        serializer1 = SaveUserSerializer(data=request.POST)
        if serializer1.is_valid():
            serializer1.update(
                instance=request.user,
                validated_data=serializer1.data
            )
        return Response(data={'result': 'Данные успешно обновлены'})


class SecurityUserViewSet(viewsets.ViewSet):
    serializer_class = SaveProfileSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        data = {'result': 'Расширенная информация о пользователе'}
        return Response(data)

    def post(self, request):
        serializer = SaveProfileSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.update(
                validated_data=serializer.data,
                instance=request.user.user_profile
            )
        return Response(data={'result': 'Вы успешно изменили данные'})


class DeleteUserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        self.request.user.delete()
        return HttpResponseRedirect(f'http://{os.environ.get("LOCALE_URL")}/')

    def list(self, request):
        return Response(data={'result': 'Удаление пользователя'})

