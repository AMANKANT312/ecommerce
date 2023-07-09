from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
    path('', views.Productview.as_view(), name= "home"),
    path('product-detail/<int:pk>', views.product_detail, name='product-detail'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart,name='cart'),
    path('pluscart/', views.plus_cart,name='pluscart'),
    path('minuscart/', views.minus_cart,name='minuscart'),
    path('remove-item/', views.remove_item,name='remove-item'),

    path('checkout/', views.checkout, name='checkout'),
    
    path('buy/', views.buy_now, name='buy-now'),
    path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('changepassword/', views.change_password, name='changepassword'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    # path('login/', views.login, name='login'),
    path("accounts/login/", auth_views.LoginView.as_view(template_name = 'app/login.html',authentication_form=LoginForm), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # path('registration/', views.customerregistration, name='customerregistration'),

   

    path('registration/',views.CustomerRegistrationView.as_view(), name='customerregistration')
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
