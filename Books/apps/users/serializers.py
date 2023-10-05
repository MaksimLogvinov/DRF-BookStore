from django.utils.translation import gettext
from rest_framework import serializers

from apps.products.models import Products
from apps.users.models import CustomUser, Profile


class LoginUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        label=gettext('Пароль'),
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = ('email',)


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=gettext('Почта'),
        required=True
    )
    password1 = serializers.CharField(
        label=gettext('Пароль'),
        required=True
    )
    password2 = serializers.CharField(
        label=gettext('Повтор пароля'),
        required=True
    )

    def create(self, validated_data):
        if validated_data['password1'] != validated_data['password2']:
            raise serializers.ValidationError('Пароли не совпадают')

        user = CustomUser(
            email=validated_data['email'],
        )
        user.is_active = False
        user.set_password(validated_data['password1'])
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(
        label=gettext('Новый пароль'),
        allow_null=False, allow_blank=False
    )
    new_password2 = serializers.CharField(
        label=gettext('Подтверждение нового пароля'),
        allow_null=False, allow_blank=False
    )


class SaveProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone_number', 'birth_date', 'country', 'city', 'id']

    def update(self, instance, validated_data):
        instance.phone_number = validated_data['phone_number']
        instance.birth_date = validated_data['birth_date']
        instance.birth_date = validated_data['birth_date']
        instance.country = validated_data['country']
        instance.city = validated_data['city']
        instance.save()
        return instance


class SaveUserSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.save()
        return instance

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']


class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name']


class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
        lookup_field = 'slug'
