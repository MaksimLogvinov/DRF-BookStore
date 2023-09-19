from django.utils.translation import gettext
from rest_framework import serializers

from apps.users.models import CustomUser


class LoginUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        label=gettext("Пароль"),
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = ('email',)


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=gettext("Почта"),
        required=True
    )
    password1 = serializers.CharField(
        label=gettext("Пароль"),
        required=True
    )
    password2 = serializers.CharField(
        label=gettext("Повтор пароля"),
        required=True
    )

    def create(self, validated_data):
        if validated_data['password1'] != validated_data['password2']:
            raise serializers.ValidationError("Пароли не совпадают")

        user = CustomUser(
            email=validated_data['email'],
        )
        user.is_active = False
        user.set_password(validated_data['password1'])
        user.save()
        return user
