import pytest
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.test import APIClient

from apps.users.models import CustomUser

client = APIClient()


@pytest.fixture(scope='function')
@pytest.mark.django_db
def create_user():
    user = CustomUser.objects.create(
        email='test@gmail.com',
        password='123456',
        username='mak'
    )
    return user


@pytest.mark.django_db
def test_register_user():
    user_data = dict(email='test@gmail.com', password='123456')
    response = client.post(
        '/user/register/', user_data
    )
    assert response.status_code == 200

    response = client.get('/user/register/')
    assert response.status_code == 200
    assert response.data['title'] == 'Страница регистрации'


@pytest.mark.django_db
def test_login_user(create_user):
    response = client.post(
        '/auth/login/', data=dict(
            email=create_user.email,
            password=create_user.password
        )
    )
    assert response.status_code == 200

    response = client.get('/auth/login/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_confirm_email(create_user):
    user = create_user
    client.force_authenticate(user=user)
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    response = client.get(f'/user/confirm-email/{uid}/{token}/')
    assert response.status_code == 200
    assert response.data['result'] == 'Ваш электронный адрес успешно активирован'


@pytest.mark.django_db
def validate_change_password(create_user):
    user = create_user
    client.force_authenticate(user=user)
    uidb64 = default_token_generator.make_token(user)
    token = urlsafe_base64_encode(force_bytes(user.pk))
    response = client.get(f'/user/reset-password/{uidb64}/{token}/')
    return response.status_code == 200


@pytest.mark.django_db
def test_change_password(create_user):
    user = create_user
    client.force_authenticate(user=user)
    uidb64 = default_token_generator.make_token(user)

    response = client.get(f'/user/reset-password/{uidb64}/done/')
    assert response.status_code == 200
    assert response.data['result'] == 'Смена пароля'

    data_change_pass = dict(new_password1='1234', new_password2='1234')
    response = client.post(
        f'/user/reset-password/{uidb64}/done/',
        data=data_change_pass
    )
    assert response.status_code == 200
    assert response.data['result'] == 'Ваш пароль был успешно изменён'


@pytest.mark.django_db
def test_profile_user(create_user):
    client.force_authenticate(user=create_user)
    response = client.get('/user/profile/')
    assert response.status_code == 200
    assert response.data['result'] == 'Информация о пользователе'

    update_profile_data = dict(first_name='pol', last_name='testova')
    response = client.post(f'/user/profile/', data=update_profile_data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_security_user(create_user):
    user = create_user
    client.force_authenticate(user=user)
    response = client.get('/user/security/')
    assert response.status_code == 200
    assert response.data['result'] == 'Расширенная информация о пользователе'

    update_user_data = dict(city='Ros', id=user.id, country='Tyu')
    response = client.post(f'/user/security/', data=update_user_data)
    assert response.status_code == 200
    assert response.data['result'] == 'Вы успешно изменили данные'


@pytest.mark.django_db
def test_delete_user(create_user):
    client.force_authenticate(user=create_user)
    response = client.delete('/user/delete/')
    assert response.status_code == 302
