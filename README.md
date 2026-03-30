# 💳 Alke Wallet

Aplicación web básica de billetera virtual desarrollada en Django.
Permite a los usuarios registrarse, iniciar sesión, ver su saldo y realizar transferencias.

Proyecto académico con enfoque práctico y funcional.

---

## 🚀 Funcionalidades

* Registro de usuarios
* Inicio y cierre de sesión
* Dashboard con saldo disponible
* Depósitos de dinero
* Transferencias:

  * A usuarios de Alke Wallet
  * A cuentas externas (bancos)
* Historial de transacciones
* Perfil de usuario
* Panel de administración (Django Admin)
* Protección de rutas (requiere login)
* Página 404 personalizada

---

## 🛠️ Tecnologías usadas

* Python
* Django
* HTML
* CSS
* Bootstrap
* SQLite

---

## 📦 Instalación

### 1. Clonar o descargar el proyecto

```bash
git clone <url-del-repo>
cd alke_wallet_project
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

### 3. Activar entorno

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor

```bash
python manage.py runserver
```

---

## 🌐 Acceso

* App: http://127.0.0.1:8000/
* Admin: http://127.0.0.1:8000/admin/

---

## 👤 Uso básico

1. Registrarse
2. Iniciar sesión
3. Depositar dinero
4. Transferir a otro usuario o cuenta bancaria
5. Revisar historial

---

## ⚠️ Notas

* Proyecto académico (no usar en producción)
* Solo utiliza moneda CLP
* Los montos no tienen decimales
* Validaciones básicas implementadas

---

## 📌 Autor

Proyecto desarrollado como ejercicio de aprendizaje en desarrollo web con Django.
