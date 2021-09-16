from django import forms

from aments_shop.models import ProductReview


class ProductReviewForm(forms.ModelForm):
	"""Форма отзыва к фильму"""

	class Meta:
		model = ProductReview
		fields = ('customer', 'text')
