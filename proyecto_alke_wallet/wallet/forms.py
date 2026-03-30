from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CuentaDestino

class FormularioRegistro(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo electrónico')
    first_name = forms.CharField(max_length=50, required=True, label='Nombre')
    last_name = forms.CharField(max_length=50, required=True, label='Apellido')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo ya está registrado.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya existe.')
        return username

class FormularioTransferencia(forms.Form):
    cuenta_destino = forms.ModelChoiceField(
        queryset=CuentaDestino.objects.none(),
        label='Cuenta destino',
        empty_label='Selecciona una cuenta',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    monto = forms.IntegerField(
        min_value=1,
        label='Monto a transferir',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'step': '1'})
    )
    descripcion = forms.CharField(
        max_length=200, required=False, label='Descripción (opcional)',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        if usuario:
            self.fields['cuenta_destino'].queryset = CuentaDestino.objects.filter(usuario=usuario)

class FormularioDeposito(forms.Form):
    monto = forms.IntegerField(
        min_value=1,
        label='Monto a depositar',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'step': '1'})
    )
    descripcion = forms.CharField(
        max_length=200, required=False, label='Descripción (opcional)',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )

class FormularioCuentaDestino(forms.ModelForm):
    class Meta:
        model = CuentaDestino
        fields = [
            'alias', 'titular', 'rut', 'banco', 'tipo_cuenta',
            'numero_cuenta', 'correo', 'es_usuario_alke', 'usuario_alke_relacionado'
        ]
        widgets = {
            'alias': forms.TextInput(attrs={'class': 'form-control'}),
            'titular': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'banco': forms.Select(attrs={'class': 'form-select'}),
            'tipo_cuenta': forms.Select(attrs={'class': 'form-select'}),
            'numero_cuenta': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'es_usuario_alke': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'usuario_alke_relacionado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        usuario_actual = kwargs.pop('usuario_actual', None)
        super().__init__(*args, **kwargs)
        queryset = User.objects.all().order_by('username')
        if usuario_actual:
            queryset = queryset.exclude(id=usuario_actual.id)
        self.fields['usuario_alke_relacionado'].queryset = queryset
        self.fields['usuario_alke_relacionado'].required = False
        self.fields['correo'].required = False

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('es_usuario_alke') and not cleaned_data.get('usuario_alke_relacionado'):
            self.add_error('usuario_alke_relacionado', 'Debes seleccionar un usuario de AlkeWallet.')
        return cleaned_data
