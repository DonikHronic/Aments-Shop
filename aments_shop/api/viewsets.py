import json
from datetime import datetime, timedelta

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .serializers import ProductSerializer, CategorySerializer
from aments_shop.favorites import ShoppingCart
from aments_shop.models import Product, ProductAnalytics, Category


class CommandFilter:
	@staticmethod
	def get_new_deliveries():
		return Product.objects.filter(date__gte=datetime.today() - timedelta(days=7))

	@staticmethod
	def get_popular_product():
		popular_products_list = [product.product.id for product in ProductAnalytics.objects.filter(views__gte=10)[:10]]
		return Product.objects.filter(id__in=popular_products_list)

	@staticmethod
	def get_related_products():
		pass

	@staticmethod
	def get_product_on_sale():
		return Product.objects.filter(sale__isnull=False)


class ProductFilter(CommandFilter):
	FILTERS_LIST = {
		'new_deliveries': CommandFilter.get_new_deliveries,
		'popular_product': CommandFilter.get_popular_product,
		'get_related_products': CommandFilter.get_related_products,
		'product_on_sale': CommandFilter.get_product_on_sale,
	}

	def __init__(self, request):
		self.request = request

	@classmethod
	def get_filters(cls):
		return [key for key in cls.FILTERS_LIST.keys()]

	def get_queryset(self):
		return self.FILTERS_LIST[self.request]()


@api_view(['GET'])
def get_products(request) -> Response:
	"""
	Получаем отфильтрованные продукты
	:param request: Запрос
	:return: Response
	"""

	filtered_products = ProductFilter(request.GET.get('filter', ''))
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
	return JsonResponse(json.dumps(ProductFilter.get_filters()), content_type='application/json', safe=False)


class ProductApiView(generics.ListCreateAPIView):
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
	Корзина пользователя
	:param request:
	:return: Возвращает страницу корзины
	"""
	cart = ShoppingCart(request)
	return render(request, 'aments_shop/cart.html', {'shopping_cart': cart})
