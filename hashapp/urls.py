from django.urls import path
from . import views

urlpatterns = [
    path('home_page/',views.home_page),
    path('register/',views.register),
    path('login/',views.login),
    path('update/',views.update)
]