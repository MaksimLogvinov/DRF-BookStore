from django.urls import path
from rest_framework_swagger.views import get_swagger_view

from apps.categories.views import (
    MagazineCatalogView, ShowBooksView, ShowMagazinesView, ShowTextbooksView,
    SearchResultView)

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path(r'^$', schema_view),
    path(
        "",
        MagazineCatalogView.as_view(),
        name="magazine_catalog"
    ),
    path(
        "books/",
        ShowBooksView.as_view(),
        name="books"
    ),
    path(
        "magazines/",
        ShowMagazinesView.as_view(),
        name="magazines"
    ),
    path(
        "textbooks/",
        ShowTextbooksView.as_view(),
        name="textbooks"
    ),
    path(
        "search/",
        SearchResultView.as_view(),
        name="search"
    ),
]
