from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

from apps.main.views import HomePage

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path(r'swagger/', schema_view),
    path('',
         HomePage.as_view(),
         name='home_page'
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
