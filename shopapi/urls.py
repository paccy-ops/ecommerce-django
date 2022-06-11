from django.urls import path
from shopapi import views

app_name = "shopapi"

urlpatterns = [
    path('', views.ProductListCreate.as_view(), name='product_list_api'),
    path('categories', views.CategoryList.as_view(), name="categories"),
    path('cart', views.ProductInCart.as_view(), name="product_in_cart"),
    path('<slug:category_slug>', views.ProductListCreate.as_view(), name="product_by_category"),

]
