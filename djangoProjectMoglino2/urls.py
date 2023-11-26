"""
URL configuration for djangoProjectMoglino2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from moglino2_site import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name='home'),
    path('home/', views.home_view, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('uslug/', views.uslug, name='uslug'),
    path('rezid/', views.rezid, name='rezid'),
    path('about/', views.about, name='about'),
    path('inf/', views.inf, name='inf'),
    path('service/<int:service_type_id>/', views.service_by_type, name='service_by_type'),
    path('add_to_cart/<int:service_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:order_id>/', views.remove_from_cart, name='remove_from_cart'),
    # path('payment/', views.payment_form, name='payment_form'),
    # path('process_payment/', views.process_payment, name='process_payment'),
    # path('notify_telegram/', views.notify_telegram, name='notify_telegram'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('total/', views.total, name='total'),
    path('process_order/', views.process_order, name='process_order'),
    path('send_telegram_message/', views.send_telegram_message, name='send_telegram_message'),

]
