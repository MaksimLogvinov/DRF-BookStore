from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from apps.categories.views import (
    MagazineCatalogViewSet, ShowBooksViewSet, ShowMagazinesViewSet,
    ShowTextbooksViewSet, SearchResultViewSet
)

schema_view = get_swagger_view(title='Categories API')


categories_router = routers.SimpleRouter()
categories_router.register(r'books', ShowBooksViewSet, basename='books')
categories_router.register(
    r'magazines',
    ShowMagazinesViewSet,
    basename='magazines'
)
categories_router.register(
    r'textbooks',
    ShowTextbooksViewSet,
    basename='textbooks'
)
categories_router.register(
    r'search',
    SearchResultViewSet,
    basename='search'
)
categories_router.register(r'', MagazineCatalogViewSet, basename='catalog')

urlpatterns = categories_router.urls
