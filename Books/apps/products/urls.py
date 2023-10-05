from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from apps.products.views import ProductInfoViewSet

schema_view = get_swagger_view(title='Products API')


products_router = routers.SimpleRouter()
products_router.register(
    r'',
    ProductInfoViewSet,
    basename='product_info'
)
urlpatterns = products_router.urls
