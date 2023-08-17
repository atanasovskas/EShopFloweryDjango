"""
URL configuration for Flowery project.

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
from eShopFlowery.views import *
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index,name='index'),
    path('admin/', admin.site.urls),
    path('index/',index,name='index'),
    path('customer_login/', customer_login, name='customer_login'),
    path('products/', products, name='products'),
    path('all_products/', all_products, name='all_products'),
    path('description/<int:code>/', description, name='description'),
    path('favorite/',favorite, name='favorite'),
    path('order/', order, name='order'),
    path('address/', address, name='address'),
    path('customer_registration/', customer_registration, name='customer_registration'),
    path('logout/', customer_logout, name='customer_logout'),
    path('add_to_cart/<str:code>', add_to_cart, name='add_to_cart'),
    path('add_to_favorite/<str:code>', add_to_favorite, name='add_to_favorite'),
    path('view_cart/', view_cart, name='view_cart'),
    path('remove_favorite/', remove_favorite, name='remove_favorite'),
    path('remove_item/', remove_item, name='remove_item'),
    path('payment/', payment, name='payment'),
    path('finish/', finish, name='finish'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
