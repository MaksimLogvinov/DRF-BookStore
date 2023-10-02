from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from apps.products.models import Products
from apps.cart.serializer import CartAddProductSerializer


class ProductInfoView(RetrieveAPIView):
    queryset = Products.objects.all()
    serializer_class = CartAddProductSerializer

    def get(self, request, *args, **kwargs):
        product = Products.objects.filter(slug=kwargs['prod_slug'])
        return Response(data={
            'result': 'Информация о товаре',
            'product': product.values()}
        )
