from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.cart.cart import Cart
from apps.cart.services import get_products
from apps.orders.models import Orders
from apps.orders.serializer import OrderCreateSerializer
from apps.orders.services import payment_order


class CreateOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderCreateSerializer
    queryset = Orders.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(data={
            'cart': get_products(Cart(request)),
            'result': 'Создание заказа'}
        )

    def post(self, request):
        result = payment_order(
            Cart(request),
            OrderCreateSerializer(data=request.POST),
            request.user
        )
        return result


class OrderSuccessViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(data={'title': 'Вы успешно оплатили заказ'})


class OrderFailedViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(data={'title': 'Оформление заказа отклонено'})
