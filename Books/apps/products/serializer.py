from rest_framework import serializers

from apps.products.models import Products, Magazines, Books, TextBooks


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class TextBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextBooks
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'


class MagazineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Magazines
        fields = '__all__'
