
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