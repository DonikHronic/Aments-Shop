from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import model_to_dict
from django.urls import reverse

from aments_shop.models_services import image_path


class CustomUser(AbstractBaseUser, PermissionsMixin):
	"""Расширенный пользователь"""

	username = models.CharField('Пользователь', max_length=25, unique=True)
	email = models.EmailField('Email', unique=True)
	date_joined = models.DateTimeField('Дата регистрации', auto_now_add=True)
	is_active = models.BooleanField('is_active', default=True)
	is_staff = models.BooleanField('is_staff', default=False)
	user_photo = models.ImageField(upload_to='users_photos/', null=True, blank=True)

	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []

	def __str__(self):
		return self.username

	class Meta:
		db_table = 'user'
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'


class Category(models.Model):
	"""Категория"""

	name = models.CharField('Категория', max_length=100, null=False)
	category_image = models.ImageField('Изображение', upload_to='category/', null=True, blank=True)
	url = models.SlugField('Ссылка', max_length=250, unique=True, null=True, blank=True)

	def __str__(self):
		return self.name

	class Meta:
		db_table = 'category'
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'


class Product(models.Model):
	"""Продукт"""

	class Colors(models.TextChoices):
		RED = 'RED', 'Красный'
		TOMATO = 'TOMATO', 'Томатный'
		GREEN = 'GREEN', 'Зеленый'
		AQUA = 'AQUA', 'Аква'
		VIOLET = 'VIOLET', 'Фиолетовый'
		WHITE = 'WHITE', 'Белый'
		BLACK = 'BLACK', 'Нигерский'
		DEFAULT = 'DEFAULT', 'По умолчанию'

	name = models.CharField('Название', max_length=150)
	description = models.TextField('Описание', max_length=500)
	preview = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name='Превью')
	price = models.PositiveSmallIntegerField('Цена', default=0)
	color = models.CharField('Цвета', choices=Colors.choices, default=Colors.DEFAULT, max_length=25)
	date = models.DateTimeField('Дата добавления', default=datetime.today)
	characteristics = models.ForeignKey(
		'Characteristic', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Характеристики'
	)
	sales = models.ForeignKey('ProductSales', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Скидка')
	category = models.ForeignKey(
		Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория',
		related_name='product_in_category'
	)
	in_stock = models.BooleanField('В наличии', default=True)
	draft = models.BooleanField('Черновик', default=True)
	url = models.SlugField('Ссылка', max_length=250, unique=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('product_detail', kwargs={'slug': self.url})

	def get_sales_price(self):
		if self.sales:
			return self.price, (self.price * (100 - self.sales.value)) / 100
		return self.price

	@staticmethod
	def get_colors():
		return Product.Colors.choices

	def to_json(self):
		return model_to_dict(self)

	def get_review(self):
		return self.productreview_set.filter(parent__isnull=True)

	class Meta:
		db_table = 'product'
		verbose_name = 'Продукт'
		verbose_name_plural = 'Продукты'
		ordering = ('date',)


class ProductAnalytics(models.Model):
	"""Аналитика продуктов"""

	product = models.ForeignKey(
		Product, on_delete=models.CASCADE, unique=True, related_name='product_views',
		verbose_name='Продукт'
	)
	views = models.IntegerField('Просмотры', default=0)

	def __str__(self):
		return f'{self.product}'

	class Meta:
		db_table = "product_analytics"
		verbose_name = 'Аналитика продукта'
		verbose_name_plural = 'Аналитика продуктов'
		ordering = ('views',)


class ProductSales(models.Model):
	"""Скидки"""

	value = models.FloatField(default=0, verbose_name='Скидка в %', unique=True)

	def __str__(self):
		return f'{self.value}'

	class Meta:
		db_table = 'product_sales'
		verbose_name = 'Скидка'
		verbose_name_plural = 'Скидки'


class ProductImages(models.Model):
	"""Изображения продукта"""

	name = models.CharField('Название', max_length=50)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
	description = models.CharField('Описание', max_length=150)
	image = models.ImageField(upload_to=image_path, verbose_name='Изображение продукта')

	def __str__(self):
		return self.name

	class Meta:
		db_table = 'product_images'
		verbose_name = 'Изображение'
		verbose_name_plural = 'Изображения'


class ProductReview(models.Model):
	"""Отзывы к продукту"""

	customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, verbose_name='Покупатель')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
	text = models.TextField('Отзыв', max_length=250)
	parent = models.ForeignKey(
		'self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Родительский отзыв'
	)

	def __str__(self):
		return f'{self.customer} - {self.text}'

	class Meta:
		db_table = 'product_review'
		verbose_name = 'Отзыв к продукту'
		verbose_name_plural = 'Отзывы к продукту'


class RatingStar(models.Model):
	"""Звезда рейтинга"""

	value = models.PositiveSmallIntegerField('Значение', default=0)

	def __str__(self):
		return f'{self.value}'

	class Meta:
		db_table = 'rating_star'
		verbose_name = 'Звезда рейтинга'
		verbose_name_plural = 'Звёзды рейтинга'


class Rating(models.Model):
	"""Рейтинг"""

	customer = models.ForeignKey(
		CustomUser, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Покупатель'
	)
	star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='Звезда')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')

	def __str__(self):
		return f'{self.customer} - {self.star}'

	class Meta:
		db_table = 'rating'
		verbose_name = 'Рейтинг'
		verbose_name_plural = 'Рейтинг'


class Characteristic(models.Model):
	"""Характеристики"""

	class CompositionType(models.TextChoices):
		STEEL = 'STEEL', 'Сталь'
		IRON = 'IRON', 'Железо'
		ALUMINIUM = 'ALUMINIUM', 'Алюминий'
		CAST_IRON = 'CAST_IRON', 'Чугун'
		POLYESTER = 'POLYESTER', 'Полиэстер'
		PLA = 'PLA', 'PLA'
		ABS = 'ABS', 'ABS'
		PETG = 'PETG', 'PETG'

	weight = models.PositiveSmallIntegerField('Вес', default=0)
	material = models.CharField('Материал', choices=CompositionType.choices, default=CompositionType.PLA, max_length=25)

	def get_material(self):
		return dict(Characteristic.CompositionType.choices)[self.material]

	def __str__(self):
		return f'{self.material}'

	class Meta:
		db_table = 'characteristic'
		verbose_name = 'Характеристика'
		verbose_name_plural = 'Характеристики'


class Customer(models.Model):
	"""Покупатель"""

	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer')
	address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, blank=True)
	first_name = models.CharField('Имя', max_length=50, null=True, blank=True)
	second_name = models.CharField('Фамилия', max_length=50, null=True, blank=True)

	def __str__(self):
		return f'{self.user}'

	class Meta:
		db_table = 'customer'
		verbose_name = 'Покупатель'
		verbose_name_plural = 'Покупатели'


class Order(models.Model):
	"""Заказ"""

	class Statuses(models.TextChoices):
		IN_PROCESSING = 'IN_PROCESSING', 'В обработке'
		ACCEPTED = 'ACCEPTED', 'Принята'
		PREPARED_FOR_SHIPMENT = 'PREPARED_FOR_SHIPMENT', 'Подготовлено к отправке'
		SENT = 'SENT', 'Отправлено',
		DELIVERED = 'DELIVERED', 'Доставлено'
		COMPLETED = 'COMPLETED', 'Завершен'

	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='Продукт')
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Заказчик')
	date = models.DateTimeField('Дата заказа', default=datetime.today)
	count = models.SmallIntegerField('Количество', default=1)
	status = models.CharField('Статус', choices=Statuses.choices, default=Statuses.IN_PROCESSING, max_length=25)

	def __str__(self):
		return f'{self.product} - {self.date} - {self.count} - {self.status}'

	class Meta:
		db_table = 'order'
		verbose_name = 'Заказ'
		verbose_name_plural = 'Заказы'


class Address(models.Model):
	"""Адрес"""

	recipient = models.CharField('Получатель', max_length=250)
	phone = models.CharField('Номер телефона', max_length=50)
	country = models.CharField('Страна', max_length=150)
	city = models.CharField('Город', max_length=150)
	location = models.CharField('Дом, кв', max_length=250)
	zip = models.CharField('Почтовый индекс', max_length=25)

	def __str__(self):
		return f'{self.country}-{self.city}-{self.location}'

	class Meta:
		db_table = 'address'
		verbose_name = 'Адрес'
		verbose_name_plural = 'Адреса'


class Post(models.Model):
	"""Пост"""

	title = models.CharField('Заголовок', max_length=250)
	author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Автор')
	preview = models.ImageField('Превью', upload_to='post_previews/')
	publish_date = models.DateTimeField('Дата публикации', default=datetime.today)
	tags = models.ManyToManyField('Tag', verbose_name='теги')
	text = models.TextField('Текст', max_length=5000)
	url = models.SlugField('Ссылка', max_length=250, unique=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post_detail', kwargs={'slug': self.url})

	def get_review(self):
		return self.postreview_set.filter(parent__isnull=True)

	class Meta:
		db_table = 'post'
		verbose_name = 'Пост'
		verbose_name_plural = 'Посты'


class Tag(models.Model):
	"""Тэг"""

	name = models.CharField('Тег', max_length=25)
	url = models.SlugField('Ссылка', max_length=250, unique=True)

	def __str__(self):
		return self.name

	class Meta:
		db_table = 'tag'
		verbose_name = 'Тег'
		verbose_name_plural = 'Теги'


class PostReview(models.Model):
	"""Отзыв к посту"""

	user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
	name = models.CharField('Имя', max_length=50)
	email = models.EmailField('Email')
	text = models.TextField('Текст', max_length=500)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
	parent = models.ForeignKey(
		'self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Родительский отзыв'
	)

	def __str__(self):
		return f'{self.name} - {self.post}'

	class Meta:
		db_table = 'post_reviews'
		verbose_name = 'Отзыв к посту'
		verbose_name_plural = 'Отзывы к посту'


@receiver(post_save, sender=CustomUser)
def save_or_create_customer(sender, instance, created, **kwargs):
	if created:
		Customer.objects.create(user=instance)
