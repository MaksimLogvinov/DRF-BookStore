from django.shortcuts import get_object_or_404

from apps.cart.serializer import CartAddProductSerializer
from apps.orders.models import Orders
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


def delete_product(cart, product_id):
    product = get_object_or_404(Products, id=product_id)
    cart.remove(product)


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
