from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.cart.cart import Cart
from apps.cart.services import get_products
from apps.orders.models import Orders
from apps.orders.serializer import OrderCreateSerializer
from apps.orders.services import show_discount, handle_order


class CreateOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Orders.objects.all().filter(ord_user_id=self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        return Response(data={
            'result': 'Создание заказа',
            'cart': get_products(Cart(request)),
            'discount': show_discount(Cart(request))
        })

    def create(self, request, *args, **kwargs):
        result = handle_order(
            Cart(request),
            OrderCreateSerializer(data=request.POST),
            request.user
        )
        return result


class OrderSuccessViewSet(viewsets.ViewSet):
    queryset = Orders.objects.all()
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        return Response(data={'title': 'Вы успешно оплатили заказ'})


class OrderFailedViewSet(viewsets.ViewSet):
    queryset = Orders.objects.all()
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        return Response(data={'title': 'Оформление заказа отклонено'})
