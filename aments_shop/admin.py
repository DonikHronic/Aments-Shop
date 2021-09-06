from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Product, ProductReview, ProductImages, Post, PostReview, Rating, RatingStar, Tag, Order, Address, \
	Customer, Characteristic, CustomUser, Category, ProductSales, ProductAnalytics


# Register your models here.
class ProductReviewInline(admin.StackedInline):
	model = ProductReview
	extra = 1


class ProductImagesInline(admin.TabularInline):
	model = ProductImages
	extra = 1
	readonly_fields = ('get_image',)

	def get_image(self, obj):
		return mark_safe(f'<img src={obj.image.url} width="150">')

	get_image.short_description = 'Изображение'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	"""Продукт"""
	list_display = ('id', 'name', 'price', 'color', 'get_preview', 'category')
	list_display_links = ('id', 'name')
	list_filter = ('characteristics__material', 'category__name')
	readonly_fields = ('get_preview',)
	search_fields = ('name', 'price', 'color', 'characteristics__material')
	inlines = [ProductImagesInline, ProductReviewInline]
	save_on_top = True
	save_as = True

	def get_preview(self, obj):
		return mark_safe(f'<img src={obj.preview.url} width="150">')

	get_preview.short_description = 'Превью'


@admin.register(ProductSales)
class ProductSalesAdmin(admin.ModelAdmin):
	pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'get_image')
	list_display_links = ('id', 'name')
	readonly_fields = ('get_image',)
	search_fields = ('name',)

	def get_image(self, obj):
		return mark_safe(f'<img src={obj.category_image.url} width="50">')

	get_image.short_description = 'Предпросмотр изображения'


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
	"""Отзыв к продукту"""
	list_display = ('id', 'customer', 'product',)
	list_filter = ('customer', 'product',)
	readonly_fields = ('customer',)
	save_as = True


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
	"""Изображения продукта"""
	list_display = ('id', 'name', 'product', 'get_image')
	readonly_fields = ('get_image',)
	save_as = True

	def get_image(self, obj):
		return mark_safe(f'<img src={obj.image.url} width="150">')

	get_image.short_description = 'Изображение'


class PostReviewInline(admin.StackedInline):
	model = PostReview
	extra = 1


@admin.register(ProductAnalytics)
class ProductAnalyticsAdmin(admin.ModelAdmin):
	list_display = ('id', 'product', 'views')
	list_display_links = ('product',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	"""Пост"""
	list_display = ('id', 'title', 'author', 'publish_date', 'preview')
	list_display_links = ('id', 'title')
	list_filter = ('author', 'tags')
	readonly_fields = ('author', 'get_preview')
	inlines = [PostReviewInline]
	save_on_top = True
	save_as = True

	def get_preview(self, obj):
		return mark_safe(f'<img src={obj.preview.url} width="150">')

	get_preview.short_description = 'Превью'


@admin.register(PostReview)
class PostReviewAdmin(admin.ModelAdmin):
	"""Отзыв к посту"""
	list_display = ('id', 'user', 'name', 'email', 'post')
	list_filter = ('post', 'user')
	readonly_fields = ('user', 'name', 'email')
	save_as = True


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
	"""Рейтинг"""
	list_display = ('id', 'star', 'customer', 'product')
	list_display_links = ('id', 'star')
	list_filter = ('customer',)
	save_as = True


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
	"""Звезда рейтинга"""
	list_display = ('id', 'value')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	"""Тэг"""
	list_display = ('id', 'name')
	list_display_links = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	"""Заказ"""
	list_display = ('id', 'product', 'user', 'date', 'status')
	list_display_links = ('id', 'product', 'user', 'status')
	list_filter = ('date', 'status')
	search_fields = ('product__name', 'user__username', 'status')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
	"""Адрес"""
	list_display = ('id', 'recipient', 'phone', 'country', 'zip')
	list_display_links = ('id', 'recipient')
	list_filter = ('country', 'zip')
	search_fields = ('recipient', 'country', 'city')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	"""Покупатель"""
	list_display = ('id', 'user', 'first_name', 'second_name', 'address')
	list_display_links = ('user', 'first_name')


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
	"""Характеристики"""
	list_display = ('id', 'material', 'weight')
	list_display_links = ('material',)
	list_filter = ('material',)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
	"""Пользователь"""
	list_display = ('username', 'email', 'date_joined', 'is_staff', 'user_photo')


admin.site.site_title = 'Aments Shop'
admin.site.site_header = 'Aments Shop'
