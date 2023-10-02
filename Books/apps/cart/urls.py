from django.urls import path
from rest_framework_swagger.views import get_swagger_view

from apps.cart.views import (
    CartDetail, HistoryOrder,
    OrderReserveView, CartAdd, CartRemove)

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path(r'^$', schema_view),
    path(
        "",
        CartDetail.as_view(),
        name="cart_detail"
    ),
    path(
        "add/<int:product_id>/",
        CartAdd.as_view(),
        name="cart_add"
    ),
    path(
        "remove/<int:product_id>/",
        CartRemove.as_view(),
        name="cart_remove"
    ),
    path(
        "history/",
        HistoryOrder.as_view(),
        name="history"
    ),
    path(
        'reserve/',
        OrderReserveView.as_view(),
        name='order_reserve'
    )
]
