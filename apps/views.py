from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from apps.models import User, Product, Category


# Create your views here.


class AlijahonHomeView(TemplateView):
    template_name = 'home.html'

class ShopView(TemplateView):
    template_name = 'shop.html'

class AccountView(TemplateView):
    template_name = 'acc.html'

class AdminMarketView(TemplateView):
    template_name = 'market.html'

class SorovTemplateView(TemplateView):
    template_name = 'sorov.html'

class HavolaTemplateView(TemplateView):
    template_name = 'havolalar.html'

class StatistikaTemplateView(TemplateView):
    template_name = 'statistika.html'

class KonkursTemplateView(TemplateView):
    template_name = 'konkurs.html'

class PayTemplateView(TemplateView):
    template_name = 'pay.html'

class ReferalTemplateView(TemplateView):
    template_name = 'referal.html'

class SettingsTemplateView(TemplateView):
    template_name = 'sozlamalar.html'

class RegisterView(View):
    def get(self, request):
        return render(request, 'home.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        cnf_password = request.POST.get('cnf_password')

        if password != cnf_password:
            messages.error(request, 'Password mos kelmadi')
            return render(request, 'home.html')

        if User.objects.filter(phone=phone).exists():  # phone_number → phone
            messages.error(request, "Bu telefon raqam allaqachon ro'yxatdan o'tgan")
            return render(request, 'home.html')

        user = User(first_name=first_name, phone=phone)  # phone_number → phone
        user.password = make_password(password)
        user.save()
        login(request, user)
        return redirect('home')

class LoginView(View):
    def get(self, request):
        return render(request, 'home.html')

    def post(self, request):
        phone_number = request.POST.get('phone')
        password = request.POST.get('password')
        queryset  = User.objects.filter(phone=phone_number)
        if queryset.exists():
            user = queryset.first()
            if user.check_password(password):
                login(request, user)
                return redirect('home')
        messages.error(request , "Telefon yoki parol noto'g'ri")
        return render(request, 'home.html')


class AllCategoriesView(ListView):
    template_name = 'base/base_shop.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.prefetch_related('images').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['new_products'] = Product.objects.prefetch_related('images').order_by('-created_at')[:20]
        context['best_seller_products'] = Product.objects.prefetch_related('images').order_by('-order_count')[:16]
        return context

class CategoryProductsView(ListView):
    template_name = 'base/base_shop.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Product.objects.filter(category=self.category).prefetch_related('images')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['new_products'] = Product.objects.prefetch_related('images').order_by('-created_at')[:20]
        context['best_seller_products'] = Product.objects.prefetch_related('images').order_by('-order_count')[:16]
        context['active_category'] = self.category
        return context

class LoginTemplateView(LoginView):
    template_name = 'login.html'
    success_url = '/'