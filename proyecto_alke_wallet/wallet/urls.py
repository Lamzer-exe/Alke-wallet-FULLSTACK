from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transacciones/', views.transacciones, name='transacciones'),
    path('transferir/', views.crear_transaccion, name='crear_transaccion'),
    path('depositar/', views.depositar, name='depositar'),
    path('perfil/', views.perfil, name='perfil'),
    path('cuentas-destino/', views.cuentas_destino, name='cuentas_destino'),
    path('cuentas-destino/agregar/', views.agregar_cuenta_destino, name='agregar_cuenta_destino'),
]
