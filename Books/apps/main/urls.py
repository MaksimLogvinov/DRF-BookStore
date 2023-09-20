from django.urls import path, include

from apps.main.views import HomePage

urlpatterns = [
    path('',
         HomePage.as_view(),
    ),
    path(
        'catalog/',
        include('apps.categories.urls')
    ),
    path(
        'cart/',
        include(('apps.cart.urls', 'apps.cart'), namespace='cart'),
    ),
    path(
        'order/',
        include('apps.orders.urls'),
    ),
    path(
        'user/',
        include('apps.users.urls')
    ),
    path(
        'product/',
        include('apps.products.urls')
    )
]