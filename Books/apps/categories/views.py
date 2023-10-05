import django_filters.rest_framework
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.response import Response

from apps.categories.services import (
    categories
)
from apps.products.models import Books, TextBooks, Magazines
from apps.products.models import Products
from apps.products.serializer import ProductSerializer, MagazineSerializer, \
    TextBookSerializer, BookSerializer


class CatalogMixin(viewsets.ModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        return Response(data={
            'product': self.serializer_class(self.get_object()).data}
        )


class SearchResultViewSet(CatalogMixin):
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['prod_title', 'slug', 'prod_description']

    def get_queryset(self):
        queryset = categories(
            model=Products.objects.all().filter(prod_quantity_on_stock__gt=0),
            user=self.request.user
        )
        return queryset

    def post(self, request):
        query = request.GET.get('search_prod')
        content = categories(
            request.GET,
            request.user,
            data=query,
        )
        return Response(data={'title': 'Поиск товара', 'content': content})


class MagazineCatalogViewSet(CatalogMixin):
    serializer_class = ProductSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    http_method_names = ['get']
    filterset_fields = [
        'prod_price', 'prod_author', 'prod_year_publication', 'prod_is_active'
    ]

    def get_queryset(self):
        queryset = categories(
            model=Products.objects.all().filter(prod_quantity_on_stock__gt=0),
            user=self.request.user
        )
        return queryset


class ShowBooksViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    http_method_names = ['get']
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = [
        'prod_price', 'book_genre',
        'prod_author', 'prod_year_publication', 'prod_is_active'
    ]

    def get_queryset(self):
        queryset = categories(
            model=Books.objects.all().filter(prod_quantity_on_stock__gt=0),
            user=self.request.user
        )
        return queryset

    def post(self, request):
        return Response(data={'content': self.queryset, 'title': 'Книги'})


class ShowMagazinesViewSet(viewsets.ModelViewSet):
    serializer_class = MagazineSerializer
    http_method_names = ['get']
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = [
        'prod_price', 'magazine_genre',
        'prod_author', 'prod_year_publication', 'prod_is_active'
    ]

    def get_queryset(self):
        queryset = categories(
            model=Magazines.objects.all().filter(prod_quantity_on_stock__gt=0),
            user=self.request.user
        )
        return queryset

    def post(self, request):
        return Response(data={'content': self.queryset, 'title': 'Журналы'})


class ShowTextbooksViewSet(viewsets.ModelViewSet):
    serializer_class = TextBookSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    http_method_names = ['get']
    filterset_fields = [
        'prod_price', 'textbook_class',
        'prod_author', 'prod_year_publication', 'prod_is_active'
    ]

    def get_queryset(self):
        queryset = categories(
            model=TextBooks.objects.all().filter(prod_quantity_on_stock__gt=0),
            user=self.request.user
        )
        return queryset

    def post(self, request):
        return Response(data={'title': 'Учебники'})
