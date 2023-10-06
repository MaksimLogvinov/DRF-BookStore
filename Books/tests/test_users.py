import pytest

from apps.users.models import CustomUser


@pytest.fixture(scope='function')
@pytest.mark.django_db
def function_fixture():
    user = CustomUser.objects.create(email='test@gmail.com', password='123456')

    print(user)
    return user


@pytest.mark.django_db
def test_1(function_fixture):
    return 1


