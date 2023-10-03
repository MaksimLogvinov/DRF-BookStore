from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse

from apps.cart.cart import Cart
from apps.cart.serializer import CartAddProductSerializer, DiscountSerializer, \
    OrderReverseSerializer, CartDeleteProductSerializer, HistoryOrderSerializer
from apps.cart.services import delete_product, update_quantity, \
    add_product, get_products
from apps.orders.models import Orders, ReservationProduct
from apps.orders.serializer import OrderCreateSerializer
from apps.orders.services import create_order
from apps.products.models import Products


class CartAddViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = CartAddProductSerializer
    lookup_field = 'pk'

    def post(self, request, *args, **kwargs):
        add_product(
            Cart(request),
            CartAddProductSerializer(data=request.POST),
            kwargs['product_id']
        )
        return HttpResponseRedirect(
            redirect_to=reverse("cart:cart_detail", request=request)
        )

    def retrieve(self, request, pk=None, *args, **kwargs):
        objects = get_object_or_404(Products, id=pk)
        return Response(objects)


class CartRemoveViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = CartDeleteProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        delete_product(Cart(request), kwargs['product_id'])
        return HttpResponseRedirect(
            redirect_to=reverse('cart:cart_detail', request=request)
        )

    def retrieve(self, request, pk=None, *args, **kwargs):
        objects = get_object_or_404(Products, id=pk)
        return Response(objects)


class CartDetailViewSet(viewsets.ViewSet):
    def get(self, request):
        return Response(data={'cart': get_products(Cart(request))})

    def post(self, request):
        cart = update_quantity(Cart(self.request))
        discount = DiscountSerializer
        content = {
            'cart': get_products(cart),
            'discount': discount,
            'title': 'Корзина'
        }
        return Response(data=content)


class HistoryOrderViewSet(viewsets.ViewSet):
    serializer_class = HistoryOrderSerializer

    def get_queryset(self):
        return Orders.objects.filter(ord_user_id=self.request.user)


class OrderReserveViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderReverseSerializer

    def get(self):
        content = {'title': 'Бронь заказа'}
        reserve = ReservationProduct.objects.filter(
            res_user_id=self.request.user
        )
        page_number = self.request.GET.get('page', 1)
        paginator = Paginator(reserve, 10)
        content['posts'] = paginator.page(page_number)
        content['reserve'] = paginator.get_page(page_number)
        return Response(data=content)

    def post(self, request, *args, **kwargs):
        serializer = OrderReverseSerializer(data=request.data)
        if serializer.is_valid():
            order = create_order(
                OrderCreateSerializer({
                    'ord_description': '-',
                    'ord_address_delivery': '-',
                    'ord_paid': '-'
                }),
                Cart(request),
                request.user
            )

            ReservationProduct.objects.create(
                res_order_id=order,
                res_user_id=request.user,
                res_time_out=serializer.data['res_time_out']
            )
            return HttpResponseRedirect(
                redirect_to=reverse('cart:order_reserve')
            )
