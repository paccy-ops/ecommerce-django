from rest_framework import serializers
from shop.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    product_url = serializers.SerializerMethodField()

    # image = serializers.URLField(read_only=True)

    class Meta:
        model = Product
        fields = ['category', 'name', 'slug', 'image',
                  'price', 'product_url', 'available', 'created', 'updated']

    @staticmethod
    def get_product_url(obj):
        product = Product.objects.get(id=obj.id)
        return product.get_absolute_url()


class ProductCartSerializer(serializers.ModelSerializer):
    product_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'slug', 'image', 'price', 'product_url']

    @staticmethod
    def get_product_url(obj):
        product = Product.objects.get(id=obj.id)
        return product.get_absolute_url()
