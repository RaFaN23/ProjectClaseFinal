from django.contrib import admin
from django.urls import path

from pizzaapp.views import *

#URL , METODO , NOMBRE
urlpatterns = [
    path('',go_home,name='home_vacio'),
    path('home/',go_home,name='home'),
]