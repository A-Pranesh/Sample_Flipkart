"""sample_flipkart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from Flipkart import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', views.registration, name='register'),
    path('login', views.login, name='login'),
    path('add_category', views.create_category, name='add_category'),
    path('add_subcategory', views.create_subcategory, name='add_subcategory'),
    path('add_product', views.create_product, name='add_product'),
    path('refresh_token', views.refresh_token, name='refresh_token'),
    path('profile', views.profile, name='profile'),
    path('get_users', views.get_users, name='get_users'),
    path('get_categories', views.get_categories, name='get_categories'),
    path('get_subcategories', views.get_subcategories, name='get_subcategories'),
    path('get_products', views.get_products, name='get_products'),
    path('get_particular_subcategory/<int:id>', views.get_particular_subcategory, name='get_particular_subcategory'),
    path('get_particular_product/<int:id>', views.get_particular_product, name='get_particular_product'),
    path('get_details', views.get_details, name='get_details')
]