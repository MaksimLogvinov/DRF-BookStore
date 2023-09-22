from django.urls import path

from apps.products.views import ProductInfoView

urlpatterns = [
    path(
        'info/<slug:prod_slug>/',
        ProductInfoView.as_view(),
        name='product_info'
    )
]
