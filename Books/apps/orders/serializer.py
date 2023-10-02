from rest_framework import serializers

from apps.orders.models import Orders


class OrderCreateSerializer(serializers.Serializer):
    ord_description = serializers.CharField(label="Комментарий")
    ord_address_delivery = serializers.CharField(label="Адрес доставки")
    ord_paid = serializers.BooleanField(label="Оплачено", required=False)
    ord_price = serializers.DecimalField(
        label='Итоговая сумма',
        required=False,
        max_digits=10,
        decimal_places=2
    )
    ord_discount = serializers.DecimalField(
        label='Скидка',
        required=False,
        max_digits=10,
        decimal_places=2
    )

    def create(self, validated_data, **kwargs):
        return Orders.objects.create(
            ord_user_id=kwargs['user'],
            **validated_data
        )
