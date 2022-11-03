from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('wmtapp.urls')),
    path('admin/', admin.site.urls),
]