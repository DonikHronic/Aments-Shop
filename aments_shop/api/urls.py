from django.urls import path

from aments_shop.api import viewsets

urlpatterns = [
	path('get_filter_list/', viewsets.get_filter_list, name='get_filter_list'),
	path('get_products/', viewsets.get_products, name='get_products'),
	path('get_popular_categories/', viewsets.get_popular_categories, name='get_popular_categories'),
	path('products-api/', viewsets.ProductApiView.as_view(), name='products-api'),
	path('accounts/cart/', viewsets.shopping_cart, name='cart_detail'),
	path('accounts/cart/add/<int:product_id>', viewsets.add_to_cart, name='add_to_cart'),
	path('accounts/cart/remove/<int:product_id>', viewsets.remove_from_cart, name='remove_from_cart'),
]
