import pytest
from rest_framework.test import APIClient

from tests.test_categories import create_book
from tests.test_users import create_user

client = APIClient()


@pytest.fixture
def add_product_cart(create_book):
    book = create_book
    client.post(f'/cart/add/{book.id}/', data=dict(quantity=2, update=1))
    return client


@pytest.mark.django_db
def test_create_order(create_user, add_product_cart):
    client = add_product_cart
    client.force_authenticate(user=create_user)
    order_data = dict(
        ord_description='descrip',
        ord_address_delivery='noneee',
        ord_paid=True,
        ord_price=234,
        ord_discount=5,
    )
    response = client.post('/order/create/', data=order_data)
    assert response.status_code == 302

    response = client.get('/order/create/')
    assert response.status_code == 200
    assert response.data['result'] == 'Создание заказа'


@pytest.mark.django_db
def test_success_order(create_user):
    client.force_authenticate(user=create_user)

    response = client.get('/order/create/success/')
    assert response.status_code == 200
    assert response.data['title'] == 'Вы успешно оплатили заказ'


@pytest.mark.django_db
def test_failed_order(create_user):
    client.force_authenticate(user=create_user)

    response = client.get('/order/create/failed/')
    assert response.status_code == 200
    assert response.data['title'] == 'Оформление заказа отклонено'
