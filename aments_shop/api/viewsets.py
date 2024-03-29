import json

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .serializers import ProductSerializer, CategorySerializer, PostsSerializer
from aments_shop.favorites import ShoppingCart
from aments_shop.models import Product, Category
from ..filters import ProductApiFilter


@api_view(['GET'])
def get_products(request) -> Response:
	"""
	Получаем отфильтрованные продукты
	:param request: Запрос
	:return: Response
	"""

	filtered_products = ProductApiFilter(request.GET.get('filter', ''))
	serializer = ProductSerializer(filtered_products.get_queryset(), many=True)
	return Response(serializer.data)


@api_view(['GET'])
def get_popular_categories(request) -> Response:
	"""
	Получаем 8 самых популярных категорий.
	:param request: Запрос
	:return: Response
	"""
	categories = Category.objects.annotate(count=Count('product_in_category')).order_by('-count')[:8]
	serializer = CategorySerializer(categories, many=True)
	return Response(serializer.data)


@api_view(['GET'])
def get_filter_list(request) -> JsonResponse:
	"""
	Получаем список фильтров для главной страницы
	:param request: Запрос
	:return: JsonResponse
	"""
	return JsonResponse(json.dumps(ProductApiFilter.get_filters()), content_type='application/json', safe=False)


@api_view(['GET'])
def get_new_posts(request) -> Response:
	"""
	Вывод последних 3 постов
	:param request:
	:return:
	"""

	filtered_posts = ProductApiFilter(request.GET.get('filter', ''))
	serializer = PostsSerializer(filtered_posts.get_queryset(), many=True)
	return Response(serializer.data)


class ProductApiView(generics.ListCreateAPIView):
	"""Список продуктов"""
	queryset = Product.objects.all()
	serializer_class = ProductSerializer


@api_view(['GET'])
def add_to_cart(request, product_id):
	"""
	Добавление в продукта в корзину через id продукта
	:param request:
	:param product_id:
	:return: После добавления перенаправляет на страницу корзины
	"""
	cart = ShoppingCart(request)
	product = get_object_or_404(Product, id=product_id)
	cart.add_or_update(product)
	return redirect('cart_detail')


@api_view(['GET'])
def remove_from_cart(request, product_id):
	"""
	Удаление продукта из корзины через id продукта
	:param request:
	:param product_id:
	:return: После удаления перенаправляет на страницу корзины
	"""
	cart = ShoppingCart(request)
	product = get_object_or_404(Product, id=product_id)
	cart.remove(product)
	return redirect('cart_detail')


@api_view(['GET'])
def shopping_cart(request):
	"""
	Корзина пользователя для API
	:param request:
	:return: Возвращает данные в виде Response
	"""
	cart = ShoppingCart(request)
	cart_items = [product for product in cart]
	total_price = 0

	for item in cart_items:
		if item['product'].sales:
			total_price += item['count'] * item['product'].price * (1 - item['product'].sales.value / 100)
		else:
			total_price += item['count'] * item['product'].price
		item['product'] = ProductSerializer(item['product']).data

	cart_items.append(round(total_price, 2))

	return Response(cart_items)
