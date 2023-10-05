from rest_framework import viewsets
from rest_framework.response import Response

from apps.products.models import Products
from apps.users.serializers import ProductInfoSerializer


class ProductInfoViewSet(viewsets.GenericViewSet):
    queryset = (
        Products.objects.all().order_by('prod_title').
        filter(prod_quantity_on_stock__gt=0))
    serializer_class = ProductInfoSerializer
    http_method_names = ['get', 'retrieve']

    def retrieve(self, request, pk=None):
        return Response(data={
            'result': 'Информация о товаре',
            'product': self.serializer_class(self.get_object()).data}
        )
