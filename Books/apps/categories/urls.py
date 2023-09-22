from django.urls import path

from apps.categories.views import (
    MagazineCatalogView, ShowBooksView, ShowMagazinesView, ShowTextbooksView,
    SearchResultView)

urlpatterns = [
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
