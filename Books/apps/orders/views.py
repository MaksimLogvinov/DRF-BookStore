from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.cart import Cart
from apps.cart.services import get_products_in_cart
from apps.orders.models import Orders
from apps.orders.serializer import OrderCreateSerializer
from apps.orders.services import payment_order


class CreateOrderView(APIView):
    serializer_class = OrderCreateSerializer
    queryset = Orders.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(data={
            "cart": get_products_in_cart(Cart(request)),
            'result': 'Создание заказа'}
        )

    def post(self, request):
        result = payment_order(
            Cart(request),
            OrderCreateSerializer(data=request.POST),
            request.user
        )
        return result


class OrderSuccessView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(data={'title': 'Вы успешно оплатили заказ'})


class OrderFailedView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(data={'title': 'Оформление заказа отклонено'})
