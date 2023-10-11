from django.shortcuts import get_object_or_404

from apps.cart.serializer import CartAddProductSerializer
from apps.orders.models import Orders, ReservationProduct
from apps.orders.serializer import OrderCreateSerializer
from apps.orders.services import create_order
from apps.products.models import Products
from apps.products.serializer import ProductSerializer


def add_product(cart, serializer, product_id):
    product = get_object_or_404(Products, id=product_id)
    if serializer.is_valid():
        cd = serializer.data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            update_quantity=cd['update']
        )


def update_quantity(cart):
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
    if serializer.is_valid():
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
        ReservationProduct.objects.create(
            res_order_id=order,
            res_user_id=user,
            res_time_out=serializer.data['res_time_out']
        )
        data = {'result': 'Заказ успешно забронирован'}
    else:
        data = {'errors': serializer.errors}
    return data
