
from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.


class AlijahonHomeView(TemplateView):
    template_name = 'home.html'

class ShopView(TemplateView):
    template_name = 'shop.html'

class AccountView(TemplateView):
    template_name = 'acc.html'

class AdminMarketView(TemplateView):
    template_name = 'market.html'