from rest_framework import viewsets
from rest_framework.response import Response

from apps.cart.serializer import CartAddProductSerializer
from apps.products.models import Products


class ProductInfoViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = CartAddProductSerializer

    def get(self, request, *args, **kwargs):
        product = Products.objects.filter(slug=kwargs['prod_slug'])
        return Response(data={
            'result': 'Информация о товаре',
            'product': product.values()}
        )
