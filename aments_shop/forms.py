from django import forms

from aments_shop.models import ProductReview, PostReview, Customer, CustomUser


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


class CustomUserForm(forms.ModelForm):
	"""Форма пользователя"""

	class Meta:
		model = CustomUser
		fields = ('email', 'password')
		widgets = {
			'email': forms.EmailInput(attrs={'class': '', 'name': 'email'}),
			'password': forms.PasswordInput(attrs={'class': '', 'name': 'password'})
		}


class CustomerForm(forms.ModelForm):
	"""Форма покупателя"""

	class Meta:
		model = Customer
		fields = ('first_name', 'second_name')
		widgets = {
			'first_name': forms.TextInput(attrs={'class': '', 'name': 'first_name'}),
			'second_name': forms.TextInput(attrs={'class': '', 'name': 'second_name'})
		}
