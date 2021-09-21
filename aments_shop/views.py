from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from shop import settings
from .favorites import ShoppingCart
from .filters import ProductsFilterClass
from .forms import ProductReviewForm, PostReviewForm, CustomerForm, CustomUserForm
from .models import Product, CustomUser, Post, Category


def homepage(request):
	"""
	Метод для отображения главной страницы
	:param request: Объект запроса
	:return: Возвращает отрендеренную главную страницу
	"""
	return render(request, 'aments_shop/index.html')


class ProductView(ListView):
	"""Продукты"""
	paginate_by = 12

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		context['colors'] = Product.get_colors()
		context['products_count'] = Product.objects.count()
		return context

	def get_queryset(self):
		if self.request.method == 'GET':
			filter_products = ProductsFilterClass(**self.request.GET)
			return filter_products.parse_datas()
		return Product.objects.filter(draft=False)


class ProductDetailView(DetailView):
	"""Полное описание продукта"""
	model = Product
	slug_field = 'url'


def registration(request):
	"""Метод регистрации"""

	context = {}
	if request.method == 'POST':
		username = request.POST.get('username', None)
		password = request.POST.get('password', None)
		email = request.POST.get('email', None)
		user = CustomUser.objects.create(username=username, email=email)
		user.set_password(password)
		user.save()
	return redirect(settings.LOGIN_URL)


@login_required
def account(request):
	context = {}
	customer_form = CustomerForm()
	context['customer_form'] = customer_form
	user_form = CustomUserForm()
	context['user_form'] = user_form
	return render(request, 'registration/my-account.html', context)


def shopping_cart(request):
	"""
	Корзина пользователя
	:param request:
	:return: Возвращает страницу корзины
	"""
	cart = ShoppingCart(request)
	total_price = 0

	for item in cart:
		if item['product'].sales:
			total_price += item['count'] * item['product'].price * (1 - item['product'].sales.value / 100)
		else:
			total_price += item['count'] * item['product'].price

	return render(request, 'aments_shop/cart.html', {'shopping_cart': cart, 'total_price': round(total_price, 2)})


class PostView(ListView):
	"""Список всех постов"""
	model = Post
	queryset = Post.objects.all()
	paginate_by = 6


class PostDetailView(DetailView):
	"""Полное представление поста"""
	model = Post
	slug_field = 'url'


class AddProductReview(View):
	"""Добавление отзыва к продукту"""

	def post(self, request, pk):
		form = ProductReviewForm(request.POST)
		product = Product.objects.get(id=pk)
		if form.is_valid():
			form = form.save(commit=False)
			if request.POST.get('parent', None):
				form.parent_id = int(request.POST.get('parent'))
			form.product = product
			form.save()
		return redirect(product.get_absolute_url())


class AddPostReview(View):
	"""Добавленние отзыва к посту"""

	def post(self, request, pk):
		form = PostReviewForm(request.POST)
		post = Post.objects.get(id=pk)
		print(form.is_valid())
		print(request.POST)
		if form.is_valid():
			form = form.save(commit=False)
			if request.POST.get('parent', None):
				form.parent_id = int(request.POST.get('parent'))
			form.post = post
			form.save()
		return redirect(post.get_absolute_url())
