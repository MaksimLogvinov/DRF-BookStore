from django.urls import path
from rest_framework_swagger.views import get_swagger_view

from apps.products.views import ProductInfoView

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path(r'^$', schema_view),
    path(
        'info/<slug:prod_slug>/',
        ProductInfoView.as_view(),
        name='product_info'
    )
]
