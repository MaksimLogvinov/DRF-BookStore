from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from apps.cart.views import (
    CartDetailViewSet, HistoryOrderViewSet,
    OrderReserveViewSet, CartAddViewSet, CartRemoveViewSet)

schema_view = get_swagger_view(title='Cart API')

cart_router = routers.SimpleRouter()
cart_router.register(r'', CartDetailViewSet, basename='cart_detail')
cart_router.register(
    r'add/<int:product_id>',
    CartAddViewSet,
    basename='cart_add'
)
cart_router.register(
    r'remove/<int:product_id>',
    CartRemoveViewSet,
    basename='cart_remove'
)
cart_router.register(
    r'history',
    HistoryOrderViewSet,
    basename='history'
)
cart_router.register(
    r'reserve',
    OrderReserveViewSet,
    basename='order_reserve'
)
urlpatterns = cart_router.urls
