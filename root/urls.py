from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from apps.views import *
from root import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', AlijahonHomeView.as_view(), name='home'),
    path('shop/<int:pk>', CategoryProductsView.as_view(), name='category'),
    path('shop/', CategoryProductsView.as_view(), name='shop'),
    # path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('account/', AccountView.as_view(), name='account'),
    path('market/', AdminMarketView.as_view(), name='market'),
    path('request/', SorovTemplateView.as_view(), name='request'),
    path('request/<int:pk>/renew/', OrderRenewView.as_view(), name='order_renew'),
    path('request/<int:pk>/recall/', OrderRecallView.as_view(), name='order_recall'),
    path('havolalar/', HavolaTemplateView.as_view(), name='havolalar'),
    path('stats/', StatistikaTemplateView.as_view(), name='stats'),
    path('konkurs/', KonkursTemplateView.as_view(), name='konkurs'),
    path('pay/', PayTemplateView.as_view(), name='pay'),
    path('referal/', ReferalTemplateView.as_view(), name='referal'),
    path('settings/', SettingsTemplateView.as_view(), name='settings'),
    path('login', AuthViewList.as_view(), name='login'),
    path('register', AuthViewList.as_view(), name='register'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('detail/<int:pk>', ProductDetailView.as_view(), name='detail'),
    path('market/<int:pk>', AdminMarketView.as_view(), name='market_category'),
    path('stream/create/', StreamCreateView.as_view(), name='stream_create'),
    path('stream/delete/<int:pk>', StreamDeleteView.as_view(), name='delete'),
    path('order/success/', OrderSuccessView.as_view(), name='order_success'),
    path('order/<int:pk>/', OrderCreateView.as_view(), name='order_create'),
    path('success-accept', success_accept, name='success_accept'),
    path('wishlist/', wishlist_list, name='wishlist'),
    path('wishlist/add/<int:pk>/', wishlist_add, name='wishlist_add'),
    path('profile/liked-products', wishlist_list, name='wishlist'),
    path('logout/', LogoutView.as_view(), name='logout'),
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
