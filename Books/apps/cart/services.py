import datetime
import logging

from django.shortcuts import get_object_or_404

from apps.cart.serializer import CartAddProductSerializer
from apps.orders.models import Orders, ReservationProduct
from apps.orders.serializer import OrderCreateSerializer
from apps.orders.services import create_order
from apps.orders.tasks import (
    send_notification_reservation_email, send_reservation_expiration_email)
from apps.products.models import Products
from apps.products.serializer import ProductSerializer


def add_product_in_cart(cart, serializer, product_id):
    product = get_object_or_404(Products, id=product_id)
    if serializer.is_valid():
        cd = serializer.data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            update_quantity=cd['update']
        )


def update_quantity_product(cart):
    for item in cart:
        item['update_quantity_form'] = CartAddProductSerializer(
            initial={'quantity': item['quantity'], 'update': True}
        )
    return cart


def history_orders(context, user_id):
    orders = Orders.objects.filter(
        ord_user_id=user_id).order_by(
        '-ord_date_created'
    ).values()
    context.update({'title': 'История заказов', 'orders': orders})
    return context


def get_products(cart):
    products = {}
    for item in cart:
        products.update(item)
        products['product'] = ProductSerializer(item['product']).data
    return products


def order_reserve(serializer, cart, user):
    order = create_order(
        OrderCreateSerializer({
            'ord_description': '-',
            'ord_address_delivery': '-',
            'ord_paid': False,
            'ord_price': cart.get_total_price(),
            'ord_discount': 0
        }),
        cart,
        user
    )
    reserve = ReservationProduct.objects.create(
        res_order_id=order,
        res_user_id=user,
        res_time_out=serializer.data['time_out']
    )

    duration_reservation = (datetime.datetime.strptime(
        serializer.data['time_out'],
        '%Y-%m-%dT%H:%M:%S%z') - order.ord_date_created)

    send_notification_reservation_email.delay(
        reserve.res_user_id.email,
        reserve.id,
    )

    task = send_reservation_expiration_email.apply_async((
        reserve.res_user_id.email, reserve.id),
        countdown=duration_reservation.total_seconds() - 300
    )
    if not task:
        logging.log(51, 'Ошибка в запланированной задаче')

    data = {'success': 'Успешная бронь'}
    return data
