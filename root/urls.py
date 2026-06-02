"""
URL configuration for root project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.url_files import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.url_files'))
"""
from django.contrib import admin
from django.urls import path

from apps.views import *

urlpatterns = [
    path('', AlijahonHomeView.as_view(), name='home'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('account/', AccountView.as_view(), name='account'),
    path('market/', AdminMarketView.as_view(), name='market'),
    path('request/', SorovTemplateView.as_view(), name='request'),
    path('havolalar/', HavolaTemplateView.as_view(), name='havolalar'),
    path('stats/', StatistikaTemplateView.as_view(), name='stats'),
    path('konkurs/', KonkursTemplateView.as_view(), name='konkurs'),
    path('pay/', PayTemplateView.as_view(), name='pay'),
    path('referal/', ReferalTemplateView.as_view(), name='referal'),
    path('settings/', SettingsTemplateView.as_view(), name='settings'),
    path('login/', LoginTemplateView.as_view(), name='login'),
]
