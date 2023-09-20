from django.core.validators import validate_slug
from django.db import models
from django.utils.translation import gettext

from apps.main.models import Storages


class ActiveProduct(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(prod_is_active=True)


class Products(models.Model):
    prod_title = models.CharField(
        verbose_name=gettext("Название товара"),
        max_length=200,
        unique=True,
    )
    prod_description = models.TextField(
        verbose_name=gettext("Описание товара"),
        max_length=500
    )
    slug = models.SlugField(
        verbose_name=gettext("Слаг товара"),
        validators=[validate_slug],
        unique=True,
    )
    prod_price = models.DecimalField(
        verbose_name=gettext("Цена товара"),
        max_digits=8,
        decimal_places=2
    )
    prod_number_pages = models.IntegerField(
        verbose_name=gettext("Кол-во страниц")
    )
    prod_author = models.CharField(
        verbose_name=gettext("Автор"),
        max_length=200
    )
    prod_age_restriction = models.IntegerField(
        verbose_name=gettext("Возрастное ограничение"),
    )
    prod_year_publication = models.DateField(
        verbose_name=gettext("Год публикации"),
    )
    prod_quantity_on_stock = models.IntegerField(
        verbose_name=gettext("Количество на складе"),
    )
    prod_storage_id = models.ManyToManyField(
        Storages,
        verbose_name=gettext("Хранилище товара"),
    )
    prod_is_active = models.BooleanField(
        default=True,
        verbose_name=gettext("Есть в продаже")
    )
    date_created = models.DateTimeField(
        verbose_name="Дата появления отзыва",
        auto_now_add=True
    )
    date_uploaded = models.DateTimeField(
        verbose_name="Дата обновления отзыва",
        auto_now=True
    )

    active_objects = ActiveProduct()
    objects = models.Manager()

    def __str__(self):
        return self.prod_title

    class Meta:
        verbose_name = gettext("Категория товаров")
        verbose_name_plural = gettext("Категории товаров")


class Photos_product(models.Model):
    photo_link = models.ImageField(
        upload_to="product/%Y/%m/%d",
        blank=True,
        verbose_name="Ссылка на фото"
    )
    prod_photo_id = models.ForeignKey(
        Products,
        verbose_name=gettext("Номер товара"),
        on_delete=models.CASCADE,
        related_name="photos"
    )

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = gettext("Фото товара")
        verbose_name_plural = gettext("Фото товаров")


class GenresBooks(models.Model):
    genre_name = models.CharField(
        verbose_name=gettext("Название жанра"),
        max_length=200
    )
    genre_description = models.TextField(
        verbose_name=gettext("Описание жанра"),
        max_length=500
    )

    def __str__(self):
        return self.genre_name

    class Meta:
        verbose_name = gettext("Жанр книги")
        verbose_name_plural = gettext("Жанры книг")


class GenresMagazines(models.Model):
    genre_name = models.CharField(
        verbose_name=gettext("Название жанра"),
        max_length=200
    )
    genre_description = models.TextField(
        verbose_name=gettext("Описание жанра"),
        max_length=500
    )

    def __str__(self):
        return self.genre_name

    class Meta:
        verbose_name = gettext("Жанр журналов")
        verbose_name_plural = gettext("Жанры журналов")


class Books(Products):
    book_genre = models.ForeignKey(
        GenresBooks,
        verbose_name=gettext("Жанр книги"),
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.prod_title

    class Meta:
        verbose_name = gettext("Книга")
        verbose_name_plural = gettext("Книги")


class ClassesTextbooks(models.Model):
    class_type = models.CharField(
        verbose_name=gettext("Для каких классов"),
        max_length=200
    )

    def __str__(self):
        return self.class_type

    class Meta:
        verbose_name = gettext("Класс учебников")
        verbose_name_plural = gettext("Классы учебников")


class TextBooks(Products):
    textbook_class = models.ForeignKey(
        ClassesTextbooks,
        verbose_name=gettext("Для каких классов"),
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.prod_title

    class Meta:
        verbose_name = gettext("Учебник")
        verbose_name_plural = gettext("Учебники")


class Magazines(Products):
    magazine_genre = models.ForeignKey(
        GenresMagazines,
        verbose_name=gettext("Жанр журнала"),
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.prod_title

    class Meta:
        verbose_name = gettext("Журнал")
        verbose_name_plural = gettext("Журналы")
