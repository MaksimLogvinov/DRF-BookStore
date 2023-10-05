import os
from decimal import Decimal

from django.http import HttpResponseRedirect

from apps.orders.models import OrderItem
from apps.products.models import Products


def payment_order(cart, serializer, user):
    if serializer.is_valid() and len(cart) > 0:
        create_order(serializer, cart, user)
        get_cashback(user, cart)
        return HttpResponseRedirect(redirect_to='success')
    return HttpResponseRedirect(
        redirect_to='failed',
        kwargs={'errors': serializer.errors}
    )


def show_discount(cart):
    cashback_percent = int(os.environ.get('cashback_percent')) / 100
    cashback = cart.get_total_price() * Decimal(cashback_percent)
    return cashback


def get_cashback(user, cart):
    user.user_profile.balance += show_discount(cart)
    user.save()


def create_order(serializer, cart, user):
    order_items = []
    update_quantity_prod = []
    order = serializer.create(
        validated_data=serializer.data,
        user=user
    )
    for item in cart:
        order_items.append(OrderItem(
            ordit_order_id=order,
            ordit_product=item['product'],
            ordit_price=item['price'],
            ordit_quantity=item['quantity'],
        ))
        item['product'].prod_quantity_on_stock -= item['quantity']
        update_quantity_prod.append(item['product'])

    OrderItem.objects.bulk_create(order_items)
    Products.objects.bulk_update(
        update_quantity_prod,
        fields=['prod_quantity_on_stock']
    )
    cart.clear()
    return order
