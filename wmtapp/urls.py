from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('filterquestion/', views.filterquestion, name='filterquestion'),
    path('filtermeal/', views.filtermeal, name='filtermeal'),
    
    path('menu/', views.menu, name='menu'),
    path('cart/', views.cart, name='cart'),
    path('history/', views.history, name='history'),

    path('addmeal/<int:id>', views.addmeal, name='addmeal'),
    path('deletebatch/<int:id>', views.deletebatch, name='deletebatch'),
    path('mealtobatch/<int:id>', views.mealtobatch, name='mealtobatch'),
    path('carttohistory/', views.carttohistory, name='carttohistory'),
    
    path('login/', views.login, name='login'),
    path('logged/', views.logged, name='logged'),

    path('accounts/', include('django.contrib.auth.urls')),
    
    path('register/', views.register, name='register'),
]
