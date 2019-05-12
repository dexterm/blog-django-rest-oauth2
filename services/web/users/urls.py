from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'), #<-- function name is index located in views.py
]
