from django.urls import path
from .views import *

app_name = 'shop'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product_list'),
    path('<slug:category_slug>/products/', ProductListView.as_view(), name='product_list_by_category'),
    path('products/<slug:country_slug>/', ProductListView.as_view(), name='product_list_by_country'),
    path('<slug:category_slug>/products/<slug:country_slug>/',
         ProductListView.as_view(),
         name='product_list_by_category_and_by_country'),
    path('<int:id>/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]
