from django.contrib import admin
from .models import CuentaWallet, CuentaDestino, Transaccion

@admin.register(CuentaWallet)
class CuentaWalletAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'saldo', 'fecha_creacion']

@admin.register(CuentaDestino)
class CuentaDestinoAdmin(admin.ModelAdmin):
    list_display = ['alias', 'titular', 'banco', 'tipo_cuenta', 'es_usuario_alke', 'usuario']

@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario_emisor', 'cuenta_destino', 'tipo', 'monto', 'fecha']
