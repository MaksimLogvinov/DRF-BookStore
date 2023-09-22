from django.urls import path

from apps.cart.views import (
    CartDetail, HistoryOrder,
    OrderReserveView, CartAdd, CartRemove)

urlpatterns = [
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
