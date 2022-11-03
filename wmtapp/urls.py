from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('menu/', views.menu, name='menu'),
    
    path('login/', views.login, name='login'),
    
    path('accounts/', include('django.contrib.auth.urls')),
]