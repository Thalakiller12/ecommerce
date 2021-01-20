from django.contrib import admin
from django.urls import path,include
from .views import LoginView,add_to_cart
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    path('login/',LoginView.as_view(),name='login'),
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('shampo/',views.shampo,name='shampo'),
    path('serum/',views.serum,name='serum'),
    path('facepack/',views.facepack,name='facepack'),
    path('soap/',views.soap,name='soap'),
    path('logout/',auth_views.LogoutView.as_view(template_name ='practice/logout.html'),name = 'logout'),
    path('add-to-cart/<slug:slug>',views.add_to_cart,name='add_to_cart'),
    path('orders/<slug:slug>',views.orders,name='orders')
]
