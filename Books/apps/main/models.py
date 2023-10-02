from django.db import models
from django.utils.translation import gettext


class Storages(models.Model):
    stor_country = models.CharField(
        verbose_name=gettext('Страна хранилища'),
        max_length=250
    )
    stor_region = models.CharField(
        verbose_name=gettext('Регион хранилища'),
        max_length=250
    )
    stor_city = models.CharField(
        verbose_name=gettext('Город хранилища'),
        max_length=250
    )
    stor_postal_code = models.CharField(
        verbose_name=gettext('Почтовый код'),
        max_length=12
    )

    class Meta:
        unique_together = ('stor_city', 'stor_region', 'stor_country')
        verbose_name = gettext('Хранилище товаров')
        verbose_name_plural = gettext('Хранилища товаров')
