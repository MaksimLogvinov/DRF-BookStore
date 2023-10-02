from django.contrib import admin

from apps.products.models import GenresBooks, GenresMagazines, ClassesTextbooks


@admin.register(GenresBooks)
class GenresBooksAdmin(admin.ModelAdmin):
    list_display = ['id', 'genre_name', 'genre_description']
    list_filter = ['id']
    search_fields = ['genre_name', 'genre_description']


@admin.register(GenresMagazines)
class GenresMagazinesAdmin(admin.ModelAdmin):
    list_display = ['id', 'genre_name', 'genre_description']
    list_filter = ['id']
    search_fields = ['genre_name', 'genre_description']


@admin.register(ClassesTextbooks)
class ClassesAdmin(admin.ModelAdmin):
    list_display = ["id", "class_type"]
    list_filter = ['id']
    search_fields = ['genre_name', 'class_type']
