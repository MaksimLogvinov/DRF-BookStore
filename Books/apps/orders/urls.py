from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from apps.orders.views import (
    CreateOrderViewSet, OrderSuccessViewSet, OrderFailedViewSet
)

schema_view = get_swagger_view(title='Orders API')

orders_router = routers.SimpleRouter()
orders_router.register(r'create', CreateOrderViewSet, basename='create_order')
orders_router.register(
    r'create/success',
    OrderSuccessViewSet,
    basename='create_success'
)
orders_router.register(
    r'create/failed',
    OrderFailedViewSet,
    basename='create_failed'
)
urlpatterns = orders_router.urls
