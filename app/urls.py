from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('shop/', views.shop, name='shop'),
    path('shop/category/<int:pk>/', views.category, name='category'),
    path('blog/', views.blog, name="blog"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('cart/', views.cart, name="cart"),
    path('product/<int:pk>/', views.product, name='product'),
    path('login/', views.loginPage, name= 'login'),
    path('logout/', views.logoutPage, name= 'logout'),
    path('register/', views.registerPage, name= 'register'),
    path('checkout/', views.checkout, name="checkout"),
    path('user/', views.user, name="user"),
    path('cart/delete/', views.cart_delete, name='cart_delete'),
    path('cart/add/', views.cart_add, name='cart_add'),
]