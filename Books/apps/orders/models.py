from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext

from apps.products.models import Products
from apps.users.models import CustomUser
from apps.users.services import send_email


class Orders(models.Model):
    ord_user_id = models.ForeignKey(
        CustomUser,
        verbose_name=gettext('Номер пользователя'),
        on_delete=models.CASCADE
    )
    ord_date_created = models.DateTimeField(
        verbose_name=gettext('Дата создания'),
        auto_now=True,
    )
    ord_description = models.TextField(
        verbose_name=gettext('Описание'),
        blank=True,
        null=True,
        max_length=300
    )
    ord_address_delivery = models.CharField(
        verbose_name=gettext('Адрес доставки'),
        blank=False,
        max_length=150
    )
    ord_paid = models.BooleanField(
        verbose_name=gettext('Оплачено'),
        default=False,
        blank=True
    )
    ord_price = models.DecimalField(
        verbose_name=gettext('Стоимость'),
        max_digits=10,
        decimal_places=2,
    )
    ord_discount = models.DecimalField(
        verbose_name=gettext('Скидка'),
        max_digits=10,
        decimal_places=2,
        null=True
    )

    objects = models.Manager()

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        ordering = ('-ord_date_created',)
        verbose_name = gettext('Заказ')
        verbose_name_plural = gettext('Заказы')

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.linkorder.all())


class OrderItem(models.Model):
    ordit_order_id = models.ForeignKey(
        Orders,
        verbose_name=gettext('Номер заказа'),
        related_name="linkorder",
        on_delete=models.CASCADE
    )
    ordit_product = models.ForeignKey(
        Products,
        verbose_name=gettext('Товар в заказе'),
        related_name='ordprod',
        on_delete=models.CASCADE
    )
    ordit_price = models.DecimalField(
        verbose_name=gettext('Цена'),
        max_digits=8,
        decimal_places=2
    )
    ordit_quantity = models.PositiveIntegerField(
        verbose_name=gettext('Количество'),
        default=1
    )

    def get_cost(self):
        return self.ordit_price * self.ordit_quantity

    objects = models.Manager()

    class Meta:
        verbose_name = gettext('Предметы заказа')
        verbose_name_plural = gettext('Предметы заказов')


@receiver(post_save, sender=Orders)
def purchase_message(sender, instance, **kwargs):
    instance.ord_user_id.user_profile.balance -= instance.ord_discount
    send_email(
        instance.ord_user_id.email,
        'cart/history/',
        'Произошла покупка товаров',
        'Вы только что совершили покупку товаров, на сайте ')


class ReservationProduct(models.Model):
    res_order_id = models.ForeignKey(
        Orders,
        verbose_name='Заказа',
        on_delete=models.CASCADE
    )
    res_user_id = models.ForeignKey(
        CustomUser,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    res_time_created = models.DateTimeField(
        verbose_name='Дата создания бронирования',
        blank=True,
        auto_now=True
    )
    res_time_out = models.DateTimeField(
        verbose_name='До какой даты действует'
    )

    objects = models.Manager()


@receiver(post_save, sender=ReservationProduct)
def purchase_message(sender, instance, **kwargs):
    send_email(
        instance.res_user_id.email,
        'cart/reserve/',
        'Бронирование товаров',
        'Вы только что забронирвоали товары, на сайте ')
