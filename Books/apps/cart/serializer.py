from rest_framework import serializers

from apps.orders.models import ReservationProduct, Orders, OrderItem


class CartAddProductSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(
        min_value=1,
        label="Кол-во",
        initial=1,
    )
    update = serializers.BooleanField(
        required=False,
        initial=False,
    )


class CartDeleteProductSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(
        allow_null=True,
        label="Номер товара",
    )


class DiscountSerializer(serializers.Serializer):
    discount_check = serializers.BooleanField(initial=False, required=False)


class OrderReverseSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReservationProduct
        fields = ('res_time_out',)


class HistoryListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id',)


class HistoryOrderSerializer(serializers.ModelSerializer):
    products = HistoryListItemSerializer(source='linkorder')

    class Meta:
        model = Orders
        fields = (
            'id', 'ord_date_created', 'ord_description',
            'ord_address_delivery', 'ord_price', 'ord_discount', 'products'
        )
