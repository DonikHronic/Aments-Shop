from django import forms

from aments_shop.models import ProductReview, PostReview


class ProductReviewForm(forms.ModelForm):
	"""Форма отзыва к фильму"""

	class Meta:
		model = ProductReview
		fields = ('customer', 'text')


class PostReviewForm(forms.ModelForm):
	"""Форма отзыва к посту"""

	class Meta:
		model = PostReview
		fields = ('name', 'email', 'text',)
