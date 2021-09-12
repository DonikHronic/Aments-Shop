from rest_framework import serializers

from aments_shop.models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
	sales_price = serializers.SerializerMethodField(method_name='get_sales_price')

	class Meta:
		model = Product
		fields = '__all__'

	@staticmethod
	def get_sales_price(obj):
		return obj.get_sales_price()


class CategorySerializer(serializers.ModelSerializer):
	category_count = serializers.SerializerMethodField()

	class Meta:
		model = Category
		fields = ['name', 'category_image', 'url', 'category_count']

	@staticmethod
	def get_category_count(obj):
		return obj.product_in_category.count()
