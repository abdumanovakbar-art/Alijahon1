import random
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import  check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DetailView, DeleteView, FormView, CreateView, ListView
from apps.forms import PayForm, ProfileForm, RegistrationForm
from apps.models import User, Product, Category, Stream, Transaction, Order, Competition, WishList

#
# class AlijahonHomeView(ListView):
#     template_name = 'home.html'
#     model = Category
#     context_object_name = 'cate'
#
#     def get(self, request, *args, **kwargs):
#         ref_id = request.GET.get('id')
#         if ref_id:
#             request.session['join_referal_id'] = ref_id
#         return super().get(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         data['pro_data'] = Product.objects.all()
#         data['cate_data'] = Category.objects.all()
#
#         referal_id = self.request.GET.get('referal')
#         if referal_id:
#             self.request.session['referrer_id'] = referal_id
#
#         return data

class AlijahonHomeView(ListView):
    model = Category
    template_name = 'home.html'
    context_object_name = 'cate'

    def get(self, request, *args, **kwargs):
        # Referral ID ni sessiyaga yozish
        ref_id = request.GET.get('id') or request.GET.get('referal')
        if ref_id:
            request.session['join_referal_id'] = ref_id
            request.session['referrer_id'] = ref_id

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['pro_data'] = Product.objects.all()

        context['cate_data'] = context['cate']

        liked_products = []
        if self.request.user.is_authenticated:
            liked_products = list(WishList.objects.filter(
                user=self.request.user
            ).values_list('product_id', flat=True))

        context['liked_products'] = liked_products
        return context

class ShopView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'pro_data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        liked_products = []
        if self.request.user.is_authenticated:
            liked_products = list(WishList.objects.filter(
                user=self.request.user
            ).values_list('product_id', flat=True))
        context['liked_products'] = liked_products
        return context

class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'acc.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.request.user.id)  # ← o'zgartiring

        if not user.api_key:
            user.generate_api_key()

        context['user'] = user
        return context

class AdminMarketView(TemplateView):
    template_name = 'market.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['products'] = Product.objects.all()
        return data


def success_accept(request):
    if request.method == 'POST':
        product_id = request.POST['product_id']
        product = Product.objects.get(id=product_id)

        quantity = int(request.POST['quantity'])
        total_price = product.price * quantity

        order = Order.objects.create(
            product=product,
            full_name=request.POST['full_name'],
            phone_number=request.POST['phone_number'],
            quantity=quantity,
            total_price=total_price,
            status='pending'
        )
        return render(request, 'order_success.html', {'order': order})
    else:
        return redirect('home')

class OrderCreateView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)

        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        quantity = int(request.POST.get('quantity', 1))

        order = Order.objects.create(
            product=product,
            full_name=full_name,
            phone_number=phone_number,
            quantity=quantity,
            status='new',
            total_price = product.price * quantity

        )

        request.session['last_order_id'] = order.id
        return redirect('order_success')


class OrderSuccessView(View):
    def get(self, request):
        order_id = request.session.get('last_order_id')
        if not order_id:
            return redirect('home')
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'order_success.html', {'order': order})

class SorovTemplateView(TemplateView):
    template_name = 'sorov.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        orders = (Order.objects.select_related('product').order_by('-created_at'))
        selected_status = self.request.GET.get('status')
        if selected_status:
            orders = orders.filter(status=selected_status)
        context['orders'] = orders
        context['status_choices'] = Order.STATUS_CHOICES
        context['selected_status'] = selected_status
        return context


class OrderRenewView(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = 'pending'
        order.save()

        messages.success(request, "Buyurtma yangilandi")
        return redirect('request')


class OrderRecallView(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = 'cancelled'
        order.save()

        messages.success(request, "Buyurtma qaytarildi")
        return redirect('request')


class HavolaTemplateView(TemplateView):
    template_name = 'havolalar.html'
    login_url = '/login'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['streams'] = Stream.objects.filter(user=self.request.user)
        return data

class StatistikaTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'statistika.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        streams = Stream.objects.filter(user=self.request.user)
        context['streams'] = streams
        return context


class KonkursTemplateView(TemplateView):
    template_name = 'konkurs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comp = Competition.objects.last()
        context['competition'] = comp
        if comp:
            context['results'] = comp.results.all()
        return context


class PayTemplateView(LoginRequiredMixin, FormView):
    template_name = 'pay.html'
    form_class = PayForm
    success_url = '/pay/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transactions'] = Transaction.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        user = self.request.user
        transaction = form.save(commit=False)

        amount = transaction.amount
        typee = transaction.type

        # проверка баланса
        if typee == 'money' and user.balance < amount:
            messages.error(self.request, "Balansingiz yetarli emas!")
            return self.form_invalid(form)

        if typee == 'coin' and user.coins < amount:
            messages.error(self.request, "Tangangiz yetarli emas!")
            return self.form_invalid(form)

        transaction.user = user
        transaction.save()

        if typee == 'money':
            user.balance -= amount
        else:
            user.coins -= amount
        user.save()

        messages.success(self.request, "So'rovingiz qabul qilindi!")
        return super().form_valid(form)


#
# class ReferalTemplateView(LoginRequiredMixin, TemplateView):
#     template_name = 'referal.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#         if not user.referral_id:
#             user.referral_id = random.randint(10000, 99999)
#             user.save()
#         referrals = User.objects.filter(referred_by=user).order_by('-created_at')
#
#         context['referral_link'] = f"http://127.0.0.1:8000/?referal={user.referral_id}"
#         context['referrals'] = referrals
#         context['referrals_count'] = referrals.count()
#
#         return context

class ReferalTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'referal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if not user.referral_id:
            user.referral_id = random.randint(10000, 99999)
            user.save()

        referrals = User.objects.filter(referred_by=user).order_by('-date_joined')
        context['referral_link'] = f"http://127.0.0.1:8000/?id={user.referral_id}"
        context['referrals'] = referrals
        context['referrals_count'] = referrals.count()
        return context


class SettingsTemplateView(LoginRequiredMixin, FormView):
    template_name = 'sozlamalar.html'
    form_class = ProfileForm
    success_url = reverse_lazy('settings')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()

        # password change logikasi alohida emas, shu yerda bo‘lishi kerak
        new_password = self.request.POST.get('new_password')
        confirm_password = self.request.POST.get('confirm_password')

        if new_password:
            if new_password != confirm_password:
                messages.error(self.request, "Parollar mos kelmadi!")
                return self.form_invalid(form)

            if len(new_password) < 6:
                messages.error(self.request, "Parol kamida 6 ta belgidan iborat!")
                return self.form_invalid(form)

            self.request.user.set_password(new_password)
            self.request.user.save()
            update_session_auth_hash(self.request, self.request.user)

        messages.success(self.request, "Profil saqlandi!")
        return super().form_valid(form)



class RegisterView(CreateView):
    queryset = User.objects.all()
    form_class = RegistrationForm
    template_name = 'home.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cate'] = Category.objects.all()
        return data

    def form_valid(self, form):
        user = form.save(commit=False)

        referrer_id = self.request.session.get('referrer_id')
        if referrer_id:
            try:
                referrer = User.objects.get(id=referrer_id)
                user.referred_by = referrer
            except User.DoesNotExist:
                pass

        user.save()

        if 'referrer_id' in self.request.session:
            del self.request.session['referrer_id']

        login(self.request, user)
        messages.success(self.request, "Muvaffaqiyatli ro'yxatdan o'tdingiz!")
        return redirect(self.success_url)

    def form_invalid(self, form):
        for error_message in form.errors.values():
            messages.error(self.request, error_message)
        return super().form_invalid(form)

class LoginFormView(View):
    def get(self, request):
        return render(request, 'home.html')

    def post(self, request):
        phone_number = request.POST.get('phone')
        password = request.POST.get('password')
        queryset = User.objects.filter(phone=phone_number)
        if queryset.exists():
            user = queryset.first()
            if user.check_password(password):
                login(request, user)
                return redirect('home')
        messages.error(request, "Telefon yoki parol noto'g'ri")
        return render(request, 'home.html')


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
        data['cate_date'] = Category.objects.all()
        data['cate_data'] = Category.objects.all()
        return data


class StreamCreateView(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        title = request.POST.get('title')
        discount = int(request.POST.get('discount', 0))

        product = Product.objects.get(id=product_id)

        if discount >= product.price:
            messages.error(request, "Chegirma mahsulot narxidan kichik bo'lishi kerak!")
            return redirect('market')

        Stream.objects.create(
            title=title,
            product=product,
            discount=discount,
            user=request.user
        )
        messages.success(request, "Oqim muvaffaqiyatli yaratildi!")
        return redirect('market')


def All_Category(request):
    cate = Category.objects.all()
    return render(request, 'base/base.html', {'cate': cate})

class AuthViewList(View):
    def post(self, request, **kwargs):
        action = request.POST.get('action')

        if action == 'register':
            phone_number = request.POST.get('phone_number')
            password = request.POST.get('password')
            conf_password = request.POST.get('conf_password')

            user_data = User.objects.filter(phone_number=phone_number).first()
            if user_data:
                messages.error(request, "Bundey nomer allaqachon mavjud")
                return redirect('home')

            if password != conf_password:
                messages.error(request, "parol bir  biriga mos kelmadi")
                return redirect('home')

            user = User.objects.create_user(phone_number=phone_number, password=password)

            session_ref_id = request.session.get('join_referal_id')

            if session_ref_id:
                referrer = User.objects.filter(referral_id=session_ref_id).first()
                if referrer:
                    user.referred_by = referrer
                    user.save()

                del request.session['join_referal_id']

            messages.success(request, "Muffaqiyatli royxatdan otdingiz")
            login(request, user)
            return redirect('account')

        elif action == 'login':
            phone_number = request.POST.get('phone_number')
            password = request.POST.get('password')
            user_data = User.objects.filter(phone_number=phone_number).first()
            if not user_data:
                messages.error(request, "Bundey nomer mavjud emas royxatdan oting")
                return redirect('home')

            if not check_password(password, user_data.password):
                messages.error(request, "Parol xato kiritildi")
                return redirect('home')

            messages.success(request, "Hush kelibsiz")
            login(request, user_data)
            return redirect('account')

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


class HavolalarDelete(DeleteView):
    queryset = Stream.objects.all()
    template_name = 'havolalar.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('havolalar')


class StreamDeleteView(View):
    def post(self, request, pk):
        stream = Stream.objects.get(id=pk, user=request.user)
        stream.delete()
        messages.success(request, "Oqim o'chirildi!")
        return redirect('havolalar')


@login_required
def wishlist_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    obj, created = WishList.objects.get_or_create(user=request.user, product=product)
    if not created:
        obj.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def wishlist_list(request):
    wishlists = WishList.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlists': wishlists})