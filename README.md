# EntradasVirtuales

Sistema de gestión de entradas virtuales desarrollado con Django y SQLite3.

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.8+** ([Descargar Python](https://www.python.org/downloads/))
- **SQLite3** (viene incluido con Python)
- **pip** (gestor de paquetes de Python)

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/EntradasVirtuales.git
cd EntradasVirtuales
```
### 2. Crear y Activar Entorno Virtual  
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```
### 4. Configurar Base de Datos SQLite
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
### 5. Aplicar Migraciones
```bash
python manage.py migrate
```
### 6. Crear Superusuario 
```bash
python manage.py createsuperuser
```
### 7. Ejecutar el Servidor de Desarrollo   
```bash
python manage.py runserver
```
### 8. Ingresar al admin del aplicativo  
```bash
http://127.0.0.1:8000/admin/
agregar Equipos y Tribunas (solo si la base de datos no es la configurada por defecto)
```
