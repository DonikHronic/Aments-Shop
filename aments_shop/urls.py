from django.urls import path

from . import views

urlpatterns = [
	path('', views.homepage, name='home'),
	path('get_filter_list/', views.get_filter_list, name='get_filter_list'),
	path('get_products/', views.get_products, name='get_products'),
	path('get_popular_categories/', views.get_popular_categories, name='get_popular_categories'),
	path('products-api/', views.ProductApiView.as_view(), name='products-api'),
	path('products/', views.ProductView.as_view(), name='products'),
	path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
	path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]
