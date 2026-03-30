from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Q

from .models import CuentaWallet, CuentaDestino, Transaccion
from .forms import FormularioRegistro, FormularioTransferencia, FormularioDeposito, FormularioCuentaDestino

def inicio(request):
    return render(request, 'wallet/inicio.html')

def registro(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            usuario = form.save()
            CuentaWallet.objects.create(usuario=usuario, saldo=0)
            messages.success(request, 'Cuenta creada exitosamente. Ahora puedes iniciar sesión.')
            return redirect('login')
        messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = FormularioRegistro()
    return render(request, 'wallet/registro.html', {'form': form})

def login_usuario(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        usuario = authenticate(request, username=username, password=password)
        if usuario:
            login(request, usuario)
            messages.success(request, 'Inicio de sesión correcto.')
            return redirect('dashboard')
        messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'wallet/login.html')

def logout_usuario(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('inicio')

@login_required
def dashboard(request):
    cuenta, _ = CuentaWallet.objects.get_or_create(usuario=request.user, defaults={'saldo': 0})
    transacciones_recientes = Transaccion.objects.filter(
        Q(usuario_emisor=request.user) | Q(cuenta_destino__usuario_alke_relacionado=request.user)
    ).select_related('cuenta_destino').order_by('-fecha')[:5]
    cuentas_destino = CuentaDestino.objects.filter(usuario=request.user).order_by('alias')[:5]
    return render(request, 'wallet/dashboard.html', {
        'cuenta': cuenta,
        'transacciones_recientes': transacciones_recientes,
        'cuentas_destino': cuentas_destino,
    })

@login_required
def transacciones(request):
    trans = Transaccion.objects.filter(
        Q(usuario_emisor=request.user) | Q(cuenta_destino__usuario_alke_relacionado=request.user)
    ).select_related('cuenta_destino').order_by('-fecha')
    return render(request, 'wallet/transacciones.html', {'transacciones': trans})

@login_required
def cuentas_destino(request):
    cuentas = CuentaDestino.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'wallet/cuentas_destino.html', {'cuentas': cuentas})

@login_required
def agregar_cuenta_destino(request):
    if request.method == 'POST':
        form = FormularioCuentaDestino(request.POST, usuario_actual=request.user)
        if form.is_valid():
            cuenta = form.save(commit=False)
            cuenta.usuario = request.user
            cuenta.save()
            messages.success(request, 'Cuenta destino agregada correctamente.')
            return redirect('cuentas_destino')
        messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = FormularioCuentaDestino(usuario_actual=request.user)
    return render(request, 'wallet/agregar_cuenta_destino.html', {'form': form})

@login_required
def crear_transaccion(request):
    cuenta_emisor, _ = CuentaWallet.objects.get_or_create(usuario=request.user, defaults={'saldo': 0})
    if request.method == 'POST':
        form = FormularioTransferencia(request.POST, usuario=request.user)
        if form.is_valid():
            cuenta_destino = form.cleaned_data['cuenta_destino']
            monto = form.cleaned_data['monto']
            descripcion = form.cleaned_data['descripcion']

            if cuenta_destino.es_usuario_alke and cuenta_destino.usuario_alke_relacionado == request.user:
                messages.error(request, 'No puedes transferirte dinero a ti mismo.')
                return render(request, 'wallet/crear_transaccion.html', {'form': form, 'saldo_actual': cuenta_emisor.saldo})

            if cuenta_emisor.saldo < monto:
                messages.error(request, 'Saldo insuficiente para realizar la transferencia.')
                return render(request, 'wallet/crear_transaccion.html', {'form': form, 'saldo_actual': cuenta_emisor.saldo})

            with transaction.atomic():
                cuenta_emisor.saldo -= monto
                cuenta_emisor.save()

                if cuenta_destino.es_usuario_alke and cuenta_destino.usuario_alke_relacionado:
                    cuenta_receptor, _ = CuentaWallet.objects.get_or_create(
                        usuario=cuenta_destino.usuario_alke_relacionado, defaults={'saldo': 0}
                    )
                    cuenta_receptor.saldo += monto
                    cuenta_receptor.save()

                Transaccion.objects.create(
                    usuario_emisor=request.user,
                    cuenta_destino=cuenta_destino,
                    tipo='transferencia',
                    monto=monto,
                    descripcion=descripcion or 'Transferencia'
                )
            messages.success(request, 'Transferencia realizada con éxito.')
            return redirect('dashboard')
        messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = FormularioTransferencia(usuario=request.user)
    return render(request, 'wallet/crear_transaccion.html', {'form': form, 'saldo_actual': cuenta_emisor.saldo})

@login_required
def depositar(request):
    cuenta, _ = CuentaWallet.objects.get_or_create(usuario=request.user, defaults={'saldo': 0})
    if request.method == 'POST':
        form = FormularioDeposito(request.POST)
        if form.is_valid():
            monto = form.cleaned_data['monto']
            descripcion = form.cleaned_data['descripcion']
            with transaction.atomic():
                cuenta.saldo += monto
                cuenta.save()
                Transaccion.objects.create(
                    usuario_emisor=request.user,
                    tipo='deposito',
                    monto=monto,
                    descripcion=descripcion or 'Depósito'
                )
            messages.success(request, 'Depósito realizado con éxito.')
            return redirect('dashboard')
        messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = FormularioDeposito()
    return render(request, 'wallet/depositar.html', {'form': form, 'saldo_actual': cuenta.saldo})

@login_required
def perfil(request):
    cuenta, _ = CuentaWallet.objects.get_or_create(usuario=request.user, defaults={'saldo': 0})
    return render(request, 'wallet/perfil.html', {'usuario': request.user, 'cuenta': cuenta})

def custom_404(request, exception):
    return render(request, '404.html', status=404)
