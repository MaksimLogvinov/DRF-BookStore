import pytest
from rest_framework.test import APIClient

from tests.test_categories import create_book, product_data
from tests.test_orders import add_product_cart
from tests.test_users import create_user

client = APIClient()


def add_product_in_cart(create_book):
    book = create_book
    client.post(f'/cart/add/{book.id}/', data=dict(quantity=2, update=1))
    return client


@pytest.mark.django_db
def test_delete_product(add_product_cart, create_user):
    client.force_authenticate(user=create_user)
    response = client.get('/cart/remove/1/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_add(create_book, create_user):
    client.force_authenticate(user=create_user)
    book = create_book
    response = client.post(f'/cart/add/{book.id}/', data=dict(quantity=2, update=1))
    assert response.status_code == 302


@pytest.mark.django_db
def test_show_cart(product_data, create_user, create_book):
    client.force_authenticate(user=create_user)
    add_product_in_cart(create_book)
    response = client.get('/cart/')
    assert response.status_code == 200
    assert response.data['cart']['price'] == product_data['prod_price']


@pytest.mark.django_db
def test_history_cart(create_user, create_book):
    client.force_authenticate(user=create_user)
    add_product_in_cart(create_book)
    order_data = dict(
        ord_description='descrip',
        ord_address_delivery='noneee',
        ord_paid=True,
        ord_price=234,
        ord_discount=5,
    )
    response = client.post('/order/create/', data=order_data)
    assert response.status_code == 302

    response = client.get('/cart/history/')
    assert response.status_code == 200
    assert response.data['results'][0]['id'] == 1


@pytest.mark.django_db
def test_reserve_order(create_user, create_book):
    client.force_authenticate(user=create_user)
    add_product_in_cart(create_book)

    reserve_data = dict(
        res_time_out='2023-10-20',
    )
    response = client.post('/cart/reserve/', data=reserve_data)
    assert response.status_code == 302

    response = client.get('/cart/reserve/')
    assert response.status_code == 200
    assert response.data['reserve'][0]['id'] == 1
