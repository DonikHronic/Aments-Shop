from django.urls import path, include

from . import views

urlpatterns = [
	path('', views.homepage, name='home'),
	path('', include('aments_shop.api.urls')),
	path('register/', views.registration, name='registration'),
	path('accounts/', views.account, name='profile'),
	path('products/', views.ProductView.as_view(), name='products'),
	path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
	path('posts/', views.PostView.as_view(), name='posts'),
	path('posts/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]
