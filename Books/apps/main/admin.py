from django.contrib import admin

from apps.main.models import Storages


@admin.register(Storages)
class StoragesAdmin(admin.ModelAdmin):
    list_display = [
        'stor_country', 'stor_region', 'stor_city', 'stor_postal_code'
    ]
    list_display_links = ('stor_postal_code',)
    search_fields = ['stor_city', 'stor_country', 'stor_postal_code']
