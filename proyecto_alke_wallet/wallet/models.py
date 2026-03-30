from django.db import models
from django.contrib.auth.models import User

class CuentaWallet(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cuenta_wallet')
    saldo = models.PositiveIntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wallet de {self.usuario.username}"

class CuentaDestino(models.Model):
    BANCO_CHOICES = [
        ('BANCOESTADO', 'BancoEstado'),
        ('BCI', 'BCI'),
        ('SANTANDER', 'Santander'),
        ('OTRO', 'Otro'),
    ]
    TIPO_CUENTA_CHOICES = [
        ('VISTA', 'Cuenta Vista'),
        ('CORRIENTE', 'Cuenta Corriente'),
        ('CHEQUERA', 'Chequera Electrónica'),
        ('OTRO', 'Otro'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cuentas_destino')
    alias = models.CharField(max_length=50)
    titular = models.CharField(max_length=100)
    rut = models.CharField(max_length=20)
    banco = models.CharField(max_length=20, choices=BANCO_CHOICES)
    tipo_cuenta = models.CharField(max_length=20, choices=TIPO_CUENTA_CHOICES)
    numero_cuenta = models.CharField(max_length=30)
    correo = models.EmailField(blank=True, null=True)
    es_usuario_alke = models.BooleanField(default=False)
    usuario_alke_relacionado = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cuentas_destino_alke'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.alias} - {self.get_banco_display()}"

class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('deposito', 'Depósito'),
        ('transferencia', 'Transferencia'),
    ]

    usuario_emisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transacciones_enviadas')
    cuenta_destino = models.ForeignKey(
        CuentaDestino, on_delete=models.SET_NULL, null=True, blank=True, related_name='transacciones_recibidas'
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='transferencia')
    monto = models.PositiveIntegerField()
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.tipo} - {self.usuario_emisor.username} - {self.monto}"
