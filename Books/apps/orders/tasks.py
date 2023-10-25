from decimal import Decimal

from celery import shared_task

from apps.main.services import send_email


@shared_task
def reserve_products(email, reserve_id):
    send_email(
        email,
        'cart/reserve/',
        'Бронирование товаров',
        f'Вы только что забронировали товары на сайте.'
        f' \nНомер вашей брони: {reserve_id}\n Посмотреть список брони: '
    )
    return True


@shared_task
def before_end_reservation(email, reserve_id):
    send_email(
        email,
        'cart/reserve/',
        'Предупреждение об окончании бронирования',
        f'Через 5 минут у вас закончится бронирование заказа {reserve_id}'
        f'\n Перейдите, чтобы оплатить: '
    )
    return True


@shared_task
def purchase_message(instance):
    instance.ord_user_id.user_profile.balance -= Decimal(instance.ord_discount)
    send_email(
        instance.ord_user_id.email,
        'cart/history/',
        'Произошла покупка товаров',
        f'Вы только что совершили покупку товаров, на сайте.'
        f'\n Номер вашего заказа {instance.id}. Подробнее: '
    )
    return True
