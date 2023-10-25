import os
from gettext import gettext

from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import CustomUser
from apps.users.serializers import (
    UserRegisterSerializer, ChangePasswordSerializer, SaveUserSerializer,
    SaveProfileSerializer
)
from apps.users.services import register_user, confirm_email, \
    change_password, check_access, profile_update, user_update
from apps.users.tasks import change_password_task

User = get_user_model()


class RegisterUserViewSet(viewsets.ViewSet):
    serializer_class = UserRegisterSerializer
    queryset = CustomUser.objects.all()

    def list(self, request, *args, **kwargs):
        data = dict(title='Страница регистрации')
        return Response(data=data)

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        return Response(register_user(serializer))


class UserConfirmEmailView(APIView):
    def get(self, request, uidb64, token):
        return Response(confirm_email(uidb64, token, User, request))


class ResetPasswordView(APIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response()

    def post(self, request):
        content = {'text': gettext('Запрос за сброс пароля отправлен')}
        change_password_task(request.user)
        return Response(content, status=status.HTTP_200_OK)


class EmailResetPasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, uidb64, token):
        result_url = check_access(uidb64, token, User)
        return HttpResponseRedirect(redirect_to=result_url)


class ResetPasswordDoneView(APIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, uidb64):
        return Response(data={'result': 'Смена пароля'})

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        return Response(data=change_password(serializer, request))


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
        serializer = SaveUserSerializer(data=request.POST)
        data = profile_update(serializer, request.user)
        return Response(data=data)


class SecurityUserViewSet(viewsets.ViewSet):
    serializer_class = SaveProfileSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        data = {'result': 'Расширенная информация о пользователе'}
        return Response(data)

    def post(self, request):
        serializer = SaveProfileSerializer(data=request.POST)
        data = user_update(serializer, request.user.user_profile)
        return Response(data=data)


class DeleteUserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        self.request.user.delete()
        return HttpResponseRedirect(
            f'http://{os.environ.get("LOCALE_URL")}/',
            content=dict(result='Успешно удалён пользователь')
        )

    def list(self, request):
        return Response(data={'result': 'Удаление пользователя'})

