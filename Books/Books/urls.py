from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

from apps.main.urls import main_router
from apps.categories.urls import categories_router
from apps.cart.urls import cart_router
from apps.orders.urls import orders_router
from apps.users.urls import users_router
from apps.products.urls import products_router

schema_view = get_swagger_view(title='BookStore API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path('swagger/', schema_view),
    path('', include(main_router.urls)),
    path(r'catalog/', include(categories_router.urls)),
    path(
        r'cart/',
        include((cart_router.urls, 'apps.cart'), namespace='cart')
    ),
    path(r'order/', include(orders_router.urls)),
    path(r'user/', include(users_router.urls)),
    path(r'product/', include(products_router.urls))
]
