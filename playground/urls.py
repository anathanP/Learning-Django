from django.urls import path
from . import views

#URL Confs

urlpatterns = [
    path('hello/', views.say_hello)
]