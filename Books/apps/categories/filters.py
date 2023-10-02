from django_filters import FilterSet

from apps.products.models import Products, Books, Magazines, TextBooks


class CategoriesFilter(FilterSet):
    class Meta:
        model = Products
        fields = {
            'prod_price': ['lt', 'gt'],
            'prod_is_active': ['exact'],
            'prod_author': ['icontains'],
            'prod_year_publication': ["lt", 'gt']
        }


class BooksFilter(FilterSet):
    class Meta:
        model = Books
        fields = {
            'prod_price': ['lt', 'gt'],
            'prod_is_active': ['exact'],
            'prod_author': ['icontains'],
            'prod_year_publication': ["lt", 'gt'],
            'book_genre': ['exact']
        }


class MagazinesFilter(FilterSet):
    class Meta:
        model = Magazines
        fields = {
            'prod_price': ['lt', 'gt'],
            'prod_is_active': ['exact'],
            'prod_author': ['icontains'],
            'prod_year_publication': ["lt", 'gt'],
            'magazine_genre': ['exact']
        }


class TextbooksFilter(FilterSet):
    class Meta:
        model = TextBooks
        fields = {
            'prod_price': ['lt', 'gt'],
            'prod_is_active': ['exact'],
            'prod_author': ['icontains'],
            'prod_year_publication': ["lt", 'gt'],
            'textbook_class': ['exact']
        }
