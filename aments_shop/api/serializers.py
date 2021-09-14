from rest_framework import serializers

from aments_shop.models import Product, Category, Post, CustomUser


class ProductSerializer(serializers.ModelSerializer):
	sales_price = serializers.SerializerMethodField(method_name='get_sales_price')
	url = serializers.SerializerMethodField(method_name='get_absolute_url')

	class Meta:
		model = Product
		fields = '__all__'

	@staticmethod
	def get_sales_price(obj):
		return obj.get_sales_price()

	@staticmethod
	def get_absolute_url(obj):
		return obj.get_absolute_url()


class CategorySerializer(serializers.ModelSerializer):
	category_count = serializers.SerializerMethodField()

	class Meta:
		model = Category
		fields = ['name', 'category_image', 'url', 'category_count']

	@staticmethod
	def get_category_count(obj):
		return obj.product_in_category.count()


class CustomUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		fields = '__all__'


class PostsSerializer(serializers.ModelSerializer):
	author = CustomUserSerializer(read_only=True)
	url = serializers.SerializerMethodField(method_name='get_absolute_url')

	class Meta:
		model = Post
		fields = '__all__'

	@staticmethod
	def get_absolute_url(obj):
		return obj.get_absolute_url()
