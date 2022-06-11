from django.urls import path
from shop import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>', views.product_list, name="product_by_category"),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail')
]