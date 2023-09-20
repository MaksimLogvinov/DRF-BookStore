from gettext import gettext

from django.contrib.auth import get_user_model, login
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import CustomUser
from apps.users.serializers import UserRegisterSerializer
from apps.users.services import send_message

User = get_user_model()


class RegisterUserView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = CustomUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_message(
                user=user,
                url_name='confirm_email',
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
                data={"result": "Ваш электронный адрес успешно активирован"}
            )
        else:
            return Response(
                data={"result": "Почта не была подтверждена"}
            )
