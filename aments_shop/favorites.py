from aments_shop.models import Product
from shop import settings


class ProductCookies(object):
	def __init__(self, request):
		"""
		Инициализация объекта куки
		:param request: Принимает request из запроса
		"""
		self.request = request
		self.session = request.session
		cart = self.session.get(settings.SHOPPING_CART_SESSION_ID)
		if not cart:
			cart = self.session[settings.SHOPPING_CART_SESSION_ID] = {}

		self.cart = cart

	def save(self):
		"""Обновление сессии"""
		self.session.modified = True

	def add_or_update(self, product: Product):
		"""
		Добавление товара в корзину или обновление его количества
		:param product: Принимает объект продукта из базы
		"""
		product_id = str(product.id)
		count = int(self.request.GET.get('count', 1))
		if product_id not in self.cart:
			self.cart[product_id] = {
				'id': product_id,
				'name': product.name,
				'count': count
			}
		self.save()

	def remove(self, product: Product):
		"""
		Удаление товара из корзины
		:param product: Принимает объект продукта из базы
		"""
		product_id = str(product.id)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def __iter__(self):
		"""
		Перебор и возврат товаров в корзине
		"""
		products_id = self.cart.keys()
		products = Product.objects.filter(id__in=products_id)

		cart = self.cart.copy()

		for product in products:
			cart[str(product.id)]['product'] = product

		for item in cart.values():
			item['name'] = str(item['name'])
			yield item

	def clean_cart(self):
		"""
		Очистка корзины
		"""
		del self.cart[settings.SHOPPING_CART_SESSION_ID]
		self.save()


class ShoppingCart(ProductCookies):
	"""Класс корзины"""

	def __init__(self, request):
		super().__init__(request)

	def __repr__(self):
		return 'Корзина покупателя'


class WishList(ProductCookies):
	"""Класс списка желаемого"""

	def __init__(self, request):
		super().__init__(request)

	def __repr__(self):
		return 'Список желаемого покупателя'
