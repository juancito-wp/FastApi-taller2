# TechGear 🛒

Aplicación híbrida desarrollada para el **Taller 2**, compuesta por un microservicio de alto rendimiento en **FastAPI** (API REST + MongoDB Atlas) y un portal web cliente en **Django** (patrón MVT) que consume esa API.

**API en producción:** https://fastapi-taller2-qvc9.onrender.com/docs

---

## 📁 Estructura del repositorio

```
Taller 2 FastApi/
├── requirements.txt          # Dependencias de ambos proyectos
├── techgear_api/             # Microservicio FastAPI
│   ├── main.py                # Punto de entrada de la API
│   ├── database.py            # Conexión a MongoDB Atlas (Motor)
│   ├── routes/
│   │   ├── productos.py       # Endpoints CRUD de productos
│   │   └── pedidos.py         # Endpoint de creación de pedidos
│   └── schemas/
│       ├── producto.py        # Modelos Pydantic de Producto
│       └── pedido.py          # Modelos Pydantic de Pedido
└── techgear_web/              # Portal web Django (MVT)
    ├── manage.py
    ├── config/                 # Configuración del proyecto Django
    └── tienda/                 # App: catálogo y creación de pedidos
        ├── views.py
        └── templates/catalogo.html
```

## 🧰 Tecnologías

| Componente        | Stack |
|--------------------|-------|
| API                | FastAPI 0.141, Uvicorn, Pydantic 2, Motor (MongoDB async) |
| Base de datos      | MongoDB Atlas |
| Portal web         | Django 6.1 (MVT), requests |
| Despliegue         | Render |

---

## ⚙️ Requisitos previos

- Python 3.11+
- Una cuenta y clúster en [MongoDB Atlas](https://www.mongodb.com/atlas)

---

## 🚀 Puesta en marcha local

### 1. Clonar el repositorio e instalar dependencias

```bash
git clone https://github.com/juancito-wp/FastApi-taller2.git
cd "FastApi-taller2/Taller 2 FastApi"

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

### 2. Configurar variables de entorno de la API

Dentro de `techgear_api/`, crea un archivo `.env` con tu cadena de conexión de MongoDB Atlas:

```
MONGODB_URL=mongodb+srv://<usuario>:<password>@<cluster>.mongodb.net/
```

### 3. Levantar la API (FastAPI)

```bash
cd techgear_api
uvicorn main:app --reload
```

- API disponible en: `http://127.0.0.1:8000`
- Documentación interactiva (Swagger UI): `http://127.0.0.1:8000/docs`
- Verificar conexión a la base de datos: `http://127.0.0.1:8000/test-db`

### 4. Levantar el portal web (Django)

En **otra terminal**, con el entorno virtual activado:

```bash
cd techgear_web
python manage.py migrate
python manage.py runserver
```

- Portal disponible en: `http://127.0.0.1:8000` *(ajusta el puerto con `runserver 8001` si ya tienes la API corriendo en 8000)*

> ⚠️ El portal Django consume la API en `http://127.0.0.1:8000` (ver `API_URL` en `techgear_web/tienda/views.py`). Si cambias el puerto de la API, actualiza esa constante.

---

## 📡 Endpoints de la API

### Productos — `/productos`

| Método   | Ruta             | Descripción                     |
|----------|------------------|----------------------------------|
| `POST`   | `/productos/`    | Crear un producto                |
| `GET`    | `/productos/`    | Listar todos los productos       |
| `GET`    | `/productos/{id}`| Obtener un producto por ID       |
| `PATCH`  | `/productos/{id}`| Actualizar un producto           |
| `DELETE` | `/productos/{id}`| Eliminar un producto             |

### Pedidos — `/pedidos`

| Método | Ruta         | Descripción                                                        |
|--------|--------------|----------------------------------------------------------------------|
| `POST` | `/pedidos/`  | Crear un pedido (valida stock disponible y lo descuenta automáticamente) |

Ejemplo de body para crear un pedido:

```json
{
  "usuario": "juan",
  "correo": "juan@correo.com",
  "productos": [
    { "producto_id": "665f1c2e...", "cantidad": 2 }
  ]
}
```

---

## ☁️ Despliegue en Render

La API (`techgear_api`) está desplegada como **Web Service** en Render con la siguiente configuración:

| Setting            | Valor |
|---------------------|-------|
| Root Directory       | `Taller 2 FastApi` |
| Build Command        | `pip install -r requirements.txt` |
| Start Command         | `cd techgear_api && uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Variable de entorno   | `MONGODB_URL` (cadena de conexión de MongoDB Atlas) |

---

## 👤 Autor

Proyecto desarrollado por **Juan** como parte del Taller 2 (FastAPI + Django + MongoDB Atlas).
