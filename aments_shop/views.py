from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from shop import settings
from .filters import ProductsFilterClass
from .forms import ProductReviewForm
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
		return context

	def get_queryset(self):
		if self.request.method == 'GET':
			filter_products = ProductsFilterClass(**self.request.GET)
			return filter_products.parse_datas()
		return Product.objects.all()


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
	return render(request, 'registration/my-account.html', context)


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
