from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, FormView

from apps.forms import RegistrationForm, LoginForm
from apps.models import User, Product, Category


class AlijahonHomeView(ListView):
    template_name = 'home.html'
    model = Category
    context_object_name = 'cate'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['pro_data'] = Product.objects.all()
        data['cate_data'] = Category.objects.all()
        return data


class ShopView(TemplateView):
    template_name = 'shop.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cate'] = Category.objects.all()
        return data


class AccountView(TemplateView):
    template_name = 'acc.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['user'] = self.request.user
        return data

class AdminMarketView(ListView):
    template_name = 'market.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        if category_id:
            return Product.objects.filter(category_id=category_id)
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cate'] = Category.objects.all()
        return data

class SorovTemplateView(TemplateView):
    template_name = 'sorov.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cate'] = Category.objects.all()
        return data


class HavolaTemplateView(TemplateView):
    template_name = 'havolalar.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cate'] = Category.objects.all()
        return data


class StatistikaTemplateView(TemplateView):
    template_name = 'statistika.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cate'] = Category.objects.all()
        return data


class KonkursTemplateView(TemplateView):
    template_name = 'konkurs.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cate'] = Category.objects.all()
        return data


class PayTemplateView(TemplateView):
    template_name = 'pay.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cate'] = Category.objects.all()
        return data


class ReferalTemplateView(TemplateView):
    template_name = 'referal.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cate'] = Category.objects.all()
        return data


class SettingsTemplateView(TemplateView):
    template_name = 'sozlamalar.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cate'] = Category.objects.all()
        return data


class CategoryProductsView(TemplateView):
    template_name = 'shop.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        cate_it = self.kwargs.get('pk')
        if cate_it:
            data['pro_data'] = Product.objects.filter(category_id=cate_it)
            data['cate_name'] = Category.objects.filter(id=cate_it).first()
        else:
            data['pro_data'] = Product.objects.all()
        data['cate'] = Category.objects.all()
        return data


class LoginFormView(FormView):
    form_class = LoginForm
    success_url = reverse_lazy('home')
    template_name = 'home.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cate'] = Category.objects.all()
        return data

    def form_invalid(self, form):
        for error_message in form.errors.values():
            messages.error(self.request, error_message)
        return super().form_invalid(form)


class RegisterView(CreateView):
    queryset = User.objects.all()
    form_class = RegistrationForm
    template_name = 'home.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cate'] = Category.objects.all()
        return data

    def form_invalid(self, form):
        for error_message in form.errors.values():
            messages.error(self.request, error_message)
        return super().form_invalid(form)


class LogOut(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'detail.html'
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cate'] = Category.objects.all()
        return data

