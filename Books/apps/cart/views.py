import os

from django.http import HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.response import Response

from apps.cart.cart import Cart
from apps.cart.serializer import CartAddProductSerializer, \
    OrderReverseSerializer, CartDeleteProductSerializer, HistoryOrderSerializer
from apps.cart.services import add_product, get_products, order_reserve
from apps.orders.models import Orders, ReservationProduct
from apps.products.models import Products
from apps.products.serializer import ProductSerializer


class CartAddViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = CartAddProductSerializer
    http_method_names = ['get','post']
    lookup_field = 'pk'

    def post(self, request, *args, **kwargs):
        add_product(
            Cart(request),
            CartAddProductSerializer(data=request.POST),
            kwargs['pk']
        )
        return HttpResponseRedirect(f'http://{os.environ.get("LOCALE_URL")}/cart/')

    def retrieve(self, request, pk=None, *args, **kwargs):
        return Response(ProductSerializer(self.get_object()).data)


class CartRemoveViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    http_method_names = ['get']
    serializer_class = CartDeleteProductSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        cart = Cart(request)
        cart.remove(product)
        return HttpResponseRedirect(f'http://{os.environ.get("LOCALE_URL")}/cart/')


class CartDetailViewSet(viewsets.ViewSet):
    http_method_names = ['get']

    def list(self, request):
        return Response(data={'cart': get_products(Cart(request))})


class HistoryOrderViewSet(viewsets.ViewSet):
    serializer_class = HistoryOrderSerializer

    def get_queryset(self):
        return Orders.objects.filter(ord_user_id=self.request.user)

    def list(self, request):
        return Response(data={'history': self.get_queryset()})

    def retrieve(self, request, *args, **kwargs):
        return Response(data=self.get_queryset().filter(pk=kwargs['pk']))


class OrderReserveViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderReverseSerializer

    def get(self):
        reserve = ReservationProduct.objects.filter(
            res_user_id=self.request.user
        )
        content = {'title': 'Бронь заказа', 'reserve': reserve}
        return Response(data=content)

    def post(self, request, *args, **kwargs):
        serializer = OrderReverseSerializer(data=request.data)
        data = order_reserve(serializer, Cart(request), request.user)
        return HttpResponseRedirect(data=data)
