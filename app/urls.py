from django.contrib import auth
from django.contrib.auth import authenticate, views as auth_views
from django.contrib.auth.forms import AuthenticationForm 
from app.models import Product
from django.views.generic.base import TemplateView, View
from shoppingx.settings import MEDIA_ROOT
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm,MySetPasswordForm

urlpatterns = [

    path('',views.ProductView.as_view(),name="home"),
    path('product-detail/<int:pk>', views.ProductDeatilView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart,name='add-to-cart'),
    path('pluscart/',views.plus_cart,name='pluscart'),
    path('minuscart/',views.minus_cart,name='minuscart'),
    path('removecart/',views.remove_cart,name='minuscart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('topwear/', views.topwear, name='topwear'),
    path('bottomwear/', views.bottomwear, name='bottomwear'),
    path('laptop/', views.laptop, name='laptop'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('topwear/<slug:data>', views.topwear, name='topweardata'),
    path('bottomwear/<slug:data>', views.bottomwear, name='bottomweardata'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page="login"),name='logout'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone'),name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset/done',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password-reset/complete',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_confirm.html'),name='password_reset_confirm'),
    path('registration/',views.CustomerRegistrationView.as_view(),name="customerregistration"),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

