from django.urls import path
from rest_framework_swagger.views import get_swagger_view

from apps.orders.views import (
    CreateOrderView, OrderSuccessView, OrderFailedView
)

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path(r'^$', schema_view),
    path('create/', CreateOrderView.as_view()),
    path('create/success', OrderSuccessView.as_view()),
    path('create/failed', OrderFailedView.as_view()),
]
