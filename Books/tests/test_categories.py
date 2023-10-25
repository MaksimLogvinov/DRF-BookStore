import pytest
from rest_framework.test import APIClient

from apps.main.models import Storages
from apps.products.models import Books, GenresBooks, ClassesTextbooks, \
    GenresMagazines
from apps.products.models import TextBooks, Magazines
from tests.test_users import create_user

client = APIClient()


@pytest.fixture
def product_data():
    data = dict(
        prod_title='test',
        prod_description='descrip',
        slug='test',
        prod_price=246,
        prod_number_pages=45,
        prod_author='Author',
        prod_age_restriction='0',
        prod_year_publication='2000-10-10',
        prod_quantity_on_stock=23,
    )
    return data


@pytest.fixture
def create_storage():
    storage_book = Storages.objects.create(
        stor_country='opium',
        stor_region='polo',
        stor_city='orden',
        stor_postal_code='263455'
    )
    return storage_book


@pytest.fixture
def create_book(create_storage, product_data):
    genre_book = GenresBooks.objects.create(
        genre_name='test_genre',
        genre_description='descrip_test'
    )

    book = Books.objects.create(
        **product_data,
        book_genre=genre_book
    )
    book.prod_storage_id.add(create_storage.id)
    book.save()
    return book


@pytest.fixture
def create_textbook(create_storage, product_data):
    textbook_class = ClassesTextbooks.objects.create(class_type='1-3')

    textbook = TextBooks.objects.create(
        **product_data,
        textbook_class=textbook_class
    )
    textbook.prod_storage_id.add(create_storage.id)
    textbook.save()
    return textbook


@pytest.fixture
def create_magazine(create_storage, product_data):
    magazine_genre = GenresMagazines.objects.create(
        genre_name='genremag',
        genre_description='descripmag'
    )

    magazine = Magazines.objects.create(
        **product_data,
        magazine_genre=magazine_genre
    )
    return magazine


@pytest.mark.django_db
def test_books_page(create_user, create_book):
    response = client.get('/catalog/books/')
    assert response.status_code == 200
    assert response.data['results'][0]['id'] == create_book.id


@pytest.mark.django_db
def test_textbooks_page(create_user, create_textbook):
    response = client.get('/catalog/textbooks/')
    assert response.status_code == 200
    assert response.data['results'][0]['id'] == create_textbook.id


@pytest.mark.django_db
def test_magazines_page(create_user, create_magazine):
    response = client.get('/catalog/magazines/')
    assert response.status_code == 200
    assert response.data['results'][0]['id'] == create_magazine.id


@pytest.mark.django_db
def test_search_page(create_user, create_magazine):
    response = client.get('/catalog/search/')
    assert response.status_code == 200

    response = client.get(
        f'/catalog/search/?search={create_magazine.prod_title}'
    )
    assert response.status_code == 200
    assert response.data['results'][0]['prod_title'] == create_magazine.prod_title


@pytest.mark.django_db
def test_catalog_page(create_user, create_textbook):
    response = client.get('/catalog/')
    assert response.status_code == 200
    assert response.data['results'][0]['prod_title'] == create_textbook.prod_title