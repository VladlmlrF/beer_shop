from django.urls import path
from .views import *

app_name = 'shop'

urlpatterns = [
    path('', index_page, name='index_page'),
    path('products/', product_list, name='product_list'),
    path('<slug:category_slug>/products/', product_list, name='product_list_by_category'),
    path('products/<slug:country_slug>/', product_list, name='product_list_by_country'),
    path('<slug:category_slug>/products/<slug:country_slug>/',
         product_list,
         name='product_list_by_category_and_by_country'),
    path('<int:id>/<slug:slug>/', product_detail, name='product_detail'),
]
