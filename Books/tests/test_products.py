import pytest

from apps.products.models import Products
from tests.test_categories import create_book


@pytest.mark.django_db
def test_product_info(client, create_book):
    product = Products.objects.first()
    response = client.get(f'/product/{product.id}/')
    assert response.status_code == 200
    assert response.data['product']['prod_title'] == create_book.prod_title
