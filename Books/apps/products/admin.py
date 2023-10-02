from django.contrib import admin
from apps.products.models import Products, Books, Magazines, Photos_product, \
    TextBooks


class ProdStorageInline(admin.TabularInline):
    model = Products.prod_storage_id.through
    extra = 3


@admin.register(Photos_product)
class PhotosAdmin(admin.ModelAdmin):
    list_display = ['id', 'photo_link', 'prod_photo_id']


@admin.register(Products)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'prod_title', 'prod_age_restriction',
        'prod_description', 'slug',
        'prod_price', 'prod_number_pages',
        'prod_author', 'prod_year_publication',
        'prod_quantity_on_stock', 'get_tag', 'prod_is_active'
        ]
    inlines = [ProdStorageInline]
    list_filter = ('id', 'prod_is_active')

    def get_tag(self, instance):
        return [tag.stor_country for tag in instance.prod_storage_id.all()]


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = [
        'products_ptr_id', 'book_genre', 'date_created', 'date_uploaded'
    ]


@admin.register(TextBooks)
class TextBooksAdmin(admin.ModelAdmin):
    list_display = [
        'products_ptr_id', 'textbook_class', 'date_created', 'date_uploaded'
    ]


@admin.register(Magazines)
class MagazinesAdmin(admin.ModelAdmin):
    list_display = [
        'products_ptr_id', 'magazine_genre', 'date_created', 'date_uploaded'
    ]
