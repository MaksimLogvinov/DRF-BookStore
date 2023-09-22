from django.urls import path

from apps.orders.views import (
    CreateOrderView, OrderSuccessView, OrderFailedView
)

urlpatterns = [
    path('create/', CreateOrderView.as_view()),
    path('create/success', OrderSuccessView.as_view()),
    path('create/failed', OrderFailedView.as_view()),
]
