from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPage, name='MainPage'),
    
    path('Carta/', views.Carta, name='Carta'),
    
    path('GuessPage/', views.GuessPage, name='GuessPage'),
    
    path('Login/', views.Login, name='Login'),
]