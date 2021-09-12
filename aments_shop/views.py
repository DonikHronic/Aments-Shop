from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from shop import settings
from .models import Product, CustomUser


def homepage(request):
	return render(request, 'aments_shop/index.html')


class ProductView(ListView):
	model = Product
	queryset = Product.objects.all()
	paginate_by = 12


class ProductDetailView(DetailView):
	model = Product
	slug_field = 'url'


def registration(request):
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
