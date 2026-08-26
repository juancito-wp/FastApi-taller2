# TechGear - Sistema hibrido de catalogo y pedidos

Aplicacion dividida en dos servicios:

- `techgear_api`: API REST con FastAPI, Pydantic y MongoDB Atlas.
- `techgear_web`: portal MVT con Django que consume la API por HTTP.

## Requisitos

- Python 3.11 o superior
- MongoDB Atlas
- Git

## Instalacion

Desde la raiz del proyecto:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edita `.env` con tu URI privada de MongoDB Atlas. Nunca subas `.env` a GitHub.

## Variables de entorno

- `MONGODB_URL`: URI del cluster y base de datos de MongoDB Atlas.
- `FASTAPI_URL`: URL del backend para Django. Por defecto `http://127.0.0.1:8000`.
- `DJANGO_SECRET_KEY`: clave secreta del portal Django.
- `DJANGO_DEBUG`: `True` para desarrollo local o `False` en produccion.
- `DJANGO_ALLOWED_HOSTS`: hosts separados por comas.

## Ejecucion

Terminal 1, desde la raiz del proyecto:

```powershell
.\venv\Scripts\Activate.ps1
uvicorn techgear_api.main:app --reload
```

API y Swagger:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

Terminal 2, desde `techgear_web`:

```powershell
.\venv\Scripts\Activate.ps1
cd techgear_web
python manage.py migrate
python manage.py runserver 127.0.0.1:8001
```

Portal web: http://127.0.0.1:8001

## Funcionalidad

La API ofrece CRUD de productos en `/productos/`, validacion Pydantic y registro de pedidos en `/pedidos/` con validacion de productos, stock y correo. El portal Django muestra el catalogo y envia pedidos mediante formularios protegidos con CSRF.

## Pruebas rapidas

```powershell
python -m compileall techgear_api techgear_web
python techgear_web\manage.py check
```

El historial de cambios se mantiene en la rama `main`.
