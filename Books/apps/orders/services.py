import os
from decimal import Decimal

from django.db import transaction
from django.http import HttpResponseRedirect

from apps.orders.models import OrderItem
from apps.orders.tasks import send_notification_purchase_email
from apps.products.models import Products


def handle_order(cart, serializer, user):
    if serializer.is_valid() and len(cart) > 0:
        with transaction.atomic():
            instance = create_order(serializer, cart, user)
            get_cashback(user, cart)
            send_notification_purchase_email(instance)
        return HttpResponseRedirect(redirect_to='success')
    return HttpResponseRedirect(
        redirect_to='failed',
        content={'errors': serializer.errors}
    )


def show_discount(cart):
    cashback_percent = int(os.environ.get('cashback_percent')) / 100
    cashback = cart.get_total_price() * Decimal(cashback_percent)
    return cashback


def get_cashback(user, cart):
    user.user_profile.balance += show_discount(cart)
    user.save()
    return user


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
