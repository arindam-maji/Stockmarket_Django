from django.contrib import admin
from django.urls import path
from django.conf import settings           # Correct import here
from django.conf.urls.static import static
from .views import index, getData, stocks, loginView, logoutView, register

urlpatterns = [
    path('', index, name='index'),
    path('stocks/', stocks, name='stocks'),
    path('data/', getData, name='data'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path('register/', register, name='register'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
