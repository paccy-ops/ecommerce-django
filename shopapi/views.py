from shopapi import serializers
from rest_framework.views import APIView
from shop.models import Product, Category
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
from cart.cart import Cart


# Create your views here.

class ProductListCreate(APIView):
    serializer_class = serializers.ProductSerializer

    def get(self, request, category_slug=None):
        category = None
        products = Product.objects.filter(available=True)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = Product.objects.filter(category=category)
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data)


class CategoryList(APIView):
    serializer_class = serializers.CategorySerializer

    def get(self, request):
        category = Category.objects.all()
        serializer = self.serializer_class(category, many=True)
        return Response({'data': serializer.data})


class ProductInCart(APIView):
    serializer_class = serializers.ProductCartSerializer

    def get(self, request):
        # cart = request.session['cart']
        product_cart = {}
        carts = Cart(request)
        product_cart['total_price'] = carts.get_total_price()
        product_cart['products'] = data = []
        for item in carts:
            print(item['total_price'])
            product_ids = item['product'].id
            products = Product.objects.filter(id=product_ids)
            for product in products:
                serializer = self.serializer_class(product).data
                serializer['product_quantity'] = item['quantity']
                serializer['total_price'] = item['total_price']
                data.append(serializer)
        return Response({"cart": product_cart})
