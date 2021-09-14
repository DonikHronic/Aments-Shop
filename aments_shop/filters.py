import re
from datetime import datetime, timedelta

from aments_shop.models import Product, ProductAnalytics, Post


class ProductsFilterClass:
	"""Класс фильтрации продуктов"""

	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs

	def parse_datas(self):
		objects = Product.objects
		filtered_fields = ProductsFilterClass.get_model_fields(Product)
		filtering_dict = {}
		for key, value in self.kwargs.items():
			key = ''.join(re.findall(r'[a-zA-Z]+', key))

			if key in filtered_fields and key != 'price':
				filtering_dict[f'{key}__in'] = [int(val) if val.isdigit() else val for val in value]
			if key in 'price':
				filtering_dict[f'{key}__lte'] = value[0]

		return objects.filter(**filtering_dict)

	@staticmethod
	def get_model_fields(model):
		return [field.name for field in model._meta.get_fields()]


class CommandFilter:
	@staticmethod
	def get_new_deliveries():
		return Product.objects.filter(date__gte=datetime.today() - timedelta(days=7))

	@staticmethod
	def get_new_posts():
		return Post.objects.filter(publish_date__gte=datetime.today() - timedelta(days=7))[:3]

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


class ProductApiFilter(CommandFilter):
	FILTERS_LIST = {
		'new_deliveries': CommandFilter.get_new_deliveries,
		'popular_product': CommandFilter.get_popular_product,
		'get_related_products': CommandFilter.get_related_products,
		'product_on_sale': CommandFilter.get_product_on_sale,
		'get_new_posts': CommandFilter.get_new_posts,
	}

	def __init__(self, request):
		self.request = request

	@classmethod
	def get_filters(cls):
		return [key for key in cls.FILTERS_LIST.keys()]

	def get_queryset(self):
		return self.FILTERS_LIST[self.request]()
