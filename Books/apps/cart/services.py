from django.shortcuts import get_object_or_404
from django.template.defaultfilters import register, floatformat

from apps.cart.serializer import CartAddProductSerializer
from apps.orders.models import Orders
from apps.products.models import Products
from apps.products.serializer import ProductSerializer


def add_product_in_cart(cart, serializer, product_id):
    product = get_object_or_404(Products, id=product_id)
    if serializer.is_valid():
        cd = serializer.data
        cart.add(
            product=product,
            quantity=cd["quantity"],
            update_quantity=cd["update"]
        )


def delete_product_from_cart(cart, product_id):
    product = get_object_or_404(Products, id=product_id)
    cart.remove(product)


def update_quantity(cart):
    for item in cart:
        item["update_quantity_form"] = CartAddProductSerializer(
            initial={"quantity": item["quantity"], "update": True}
        )
    return cart


@register.filter
def res_price(value, sub):
    if value - sub > 1:
        result = value - sub
    else:
        result = 1
    return result


@register.filter
def discount(sub, value):
    if value - sub > 1:
        result = sub
    else:
        max_disc = sub - value
        result = sub - max_disc - 1
    return result


@register.filter
def float_num(value):
    value = floatformat(value, arg=2)
    return str(value).replace(',', '.')


def history_orders(context, user_id):
    orders = Orders.objects.filter(
        ord_user_id=user_id).order_by(
        "-ord_date_created"
    ).values()
    context.update({"title": "История заказов", 'orders': orders})
    return context


def get_products_in_cart(cart):
    products = {}
    for i in cart:
        products.update(i)
        products['product'] = ProductSerializer(i['product']).data
    return products
