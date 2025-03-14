from django.urls import  path
from .views import fetch_all_objects, fetch_product_by_name , fetch_products_by_brand , add_product , update_product , delete_product, get_csrf_token
from .controllers import *


# urlpatterns = [
#     path('products/',fetch_all_objects , name='fetch_all_objects'),
#     path('products/name/<str:product_name>/' , fetch_product_by_name , name='fetch_products_by_name'),
#     path('products/brand/<str:brand_name>/' , fetch_products_by_brand , name='fetch_products_by_brand'),
#     path('products/add/' , add_product , name='add_products'),
#     path('products/update/<str:product_name>/' , update_product , name='update_product'),
#     path('products/delete/<str:product_name>/' , delete_product , name='delete_product'),
    
#     path("get-csrf-token/", get_csrf_token , name="get_csrf_token")
# ]

urlpatterns = [
    path('products/<int:page_number>/',all_products , name='fetch_all_objects'),
    path('products/id/<str:product_id>/' , product_by_id , name='fetch_products_by_id'),
    path('products/brand/<str:brand_name>/' , product_by_brand , name='fetch_products_by_brand'),
    path('products/add_product/' , add_product , name='add_products'),
    path('products/update/<str:product_id>/' , update_product , name='update_product'),
    path('products/delete/<str:product_id>/' , delete_product , name='delete_product'),
]