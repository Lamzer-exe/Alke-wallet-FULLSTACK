from django.contrib import admin
from django.urls import path, include
from wallet import views as wallet_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('wallet.urls')),
]

handler404 = wallet_views.custom_404
