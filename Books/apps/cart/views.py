import os

from django.http import HttpResponseRedirect
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.cart.cart import Cart
from apps.cart.serializer import CartAddProductSerializer, \
    OrderReserveSerializer, CartDeleteProductSerializer, OrderSerializer, \
    ShowReserveSerializer
from apps.cart.services import add_product_in_cart, get_products, order_reserve
from apps.orders.models import Orders, ReservationProduct
from apps.products.models import Products
from apps.products.serializer import ProductSerializer


class CartAddViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = CartAddProductSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post']
    lookup_field = 'pk'

    def post(self, request, *args, **kwargs):
        add_product_in_cart(
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
    permission_classes = (IsAuthenticated,)
    serializer_class = CartDeleteProductSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        cart = Cart(request)
        cart.remove(product)
        return HttpResponseRedirect(f'http://{os.environ.get("LOCALE_URL")}/cart/')


class CartDetailViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    permission_classes = (IsAuthenticated,)
    queryset = Cart

    def list(self, request, *args, **kwargs):
        return Response(data={
            'cart': get_products(Cart(request)),
            'results': 'Товары в корзине'}
        )


class HistoryOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Orders.objects.filter(ord_user_id=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        return Response(data=self.get_queryset().filter(pk=kwargs['pk']))


class OrderReserveViewSet(viewsets.ModelViewSet):
    queryset = ReservationProduct.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderReserveSerializer

    def list(self, request, *args, **kwargs):
        serializer = ShowReserveSerializer(
            data=ReservationProduct.objects.filter(res_user_id=request.user),
            many=True
        )
        serializer.is_valid()
        content = {
            'title': 'Бронь заказа',
            'reserve': serializer.data,
            'pre_reserve': get_products(Cart(request))
        }
        return Response(data=content)

    def create(self, request, *args, **kwargs):
        serializer = OrderReserveSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'errors': f'{serializer.errors}'},
                status=status.HTTP_404_NOT_FOUND
            )
        data = order_reserve(serializer, Cart(request), request.user)
        return HttpResponseRedirect(
            content=data,
            redirect_to=f'http://{os.environ["LOCALE_URL"]}/cart/'
        )
