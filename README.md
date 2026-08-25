# ⚡ TECHGEAR

> **Tecnología que impulsa tu mundo.**

**TechGear** es una plataforma web para explorar productos tecnológicos y gestionar pedidos. Está construida con **Django, FastAPI y MongoDB Atlas**, separando el portal web de la lógica de la API REST.

---

## ✦ Sobre TechGear

La plataforma permite consultar un catálogo de productos con:

- **Nombre**
- **Descripción**
- **Categoría**
- **Precio**
- **Stock**

También permite gestionar pedidos y verificar la disponibilidad de los productos.

---

## 🔄 Arquitectura

```text
        👤 Usuario
            │
            ▼
     ┌──────────────┐
     │    Django    │
     │  Portal Web  │
     └──────┬───────┘
            │ HTTP
            ▼
     ┌──────────────┐
     │   FastAPI    │
     │   REST API   │
     └──────┬───────┘
            │
            ▼
     ┌──────────────┐
     │ MongoDB Atlas│
     │ Base de datos│
     └──────────────┘
```

- **Django** presenta el catálogo visual al usuario.
- **FastAPI** gestiona productos, pedidos y validaciones.
- **MongoDB Atlas** almacena la información de forma persistente.

---

## 🛠️ Tecnologías

| Tecnología | Función |
| --- | --- |
| 🐍 **Python** | Lenguaje principal |
| ⚡ **FastAPI** | API REST y lógica de negocio |
| 🌐 **Django** | Portal web e interfaz de usuario |
| 🗄️ **MongoDB Atlas** | Base de datos NoSQL |
| 📋 **Pydantic** | Validación de datos y esquemas |
| 🔗 **Requests** | Comunicación HTTP (Django → FastAPI) |
| 🎨 **HTML / CSS** | Diseño de interfaz |
| 📚 **Swagger UI** | Documentación interactiva de la API |
| ☁️ **Render** | Despliegue en la nube |
| 🐙 **Git / GitHub** | Control de versiones |

---
## 📁 Estructura del Proyecto

```text
Taller2_pyfastapi/
│
├── techgear_api/
│   ├── models/
│   │   ├── pedido.py
│   │   └── producto.py
│   ├── routers/
│   │   ├── pedidos.py
│   │   └── productos.py
│   ├── database.py
│   └── main.py
│
├── techgear_web/
│   ├── catalogo/
│   │   ├── static/
│   │   │   └── catalogo/
│   │   │       ├── css/
│   │   │       │   ├── inicio.css
│   │   │       │   └── productos.css
│   │   │       └── imagenes/
│   │   ├── templates/
│   │   │   └── catalogo/
│   │   │       ├── Inicio.html
│   │   │       └── productos.html
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── techgear/
│   └── manage.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

⚠️ **Importante:** `database_ambiente502.py` existe físicamente, pero **no lo pondría en la estructura principal del README** porque es un archivo antiguo/de respaldo y `database.py` es el que representa la configuración actual.

Y tampoco pondría `venv/`, `.env`, `__pycache__` ni los archivos `.pyc`, porque son archivos/carpetas que no necesitamos destacar en la estructura del proyecto.

---


## 🌐 Accesos

### ⚡ API en producción

[🚀 TechGear API](https://taller2-pyfastapi-u0hp.onrender.com/)

### 📚 Swagger UI

[📖 Documentación de la API](https://taller2-pyfastapi-u0hp.onrender.com/docs)

### 🐙 GitHub

[🔗 Repositorio de TechGear](https://github.com/rudydayanapalacios-wq/Taller2_pyfastapi)

---

## ⚙️ Instalación y Configuración

1. **Clonar el repositorio:**

```bash
git clone https://github.com/rudydayanapalacios-wq/Taller2_pyfastapi.git
cd Taller2_pyfastapi
```

2. **Crear y activar el entorno virtual (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Instalar dependencias:**

```bash
pip install -r requirements.txt
```

4. **Variables de entorno:**

Configurar las variables de entorno necesarias para MongoDB Atlas en un archivo `.env` en la raíz del proyecto.

> 🔐 El archivo `.env` y las credenciales privadas **nunca** deben publicarse ni subirse al repositorio.

---

## 💻 Ejecución Local

Para utilizar TechGear localmente, FastAPI y Django deben ejecutarse al mismo tiempo en terminales separadas.

### ⚡ FastAPI

Desde la raíz del proyecto:

```bash
uvicorn techgear_api.main:app --reload
```

- **API:** http://127.0.0.1:8000/
- **Swagger UI:** http://127.0.0.1:8000/docs

### 🌐 Django

En otra terminal:

```bash
cd techgear_web
python manage.py runserver 8001
```

- **Portal:** http://127.0.0.1:8001/
- **Catálogo:** http://127.0.0.1:8001/productos/

---

## 🔄 Flujo de Integración

Django obtiene los productos desde FastAPI de manera dinámica consumiendo los endpoints REST mediante la librería `requests`:

```text
Django (Portal Web)
   │
   │  Petición HTTP (requests)
   ▼
FastAPI (REST API)
   │
   │  Consulta / Persistencia
   ▼
MongoDB Atlas (Base de datos)
   │
   ▼
FastAPI
   │
   ▼
Django → Muestra Catálogo al Usuario
```

---

## 🛡️ Validaciones y Respuestas HTTP

FastAPI utiliza **Pydantic** para validar los datos recibidos y controlar las operaciones de productos y pedidos.

También verifica la disponibilidad de stock antes de registrar un pedido.

Ejemplo de respuesta cuando no hay suficiente stock:

```json
{
  "detail": "Stock insuficiente"
}
```

| Código | Significado |
|--------|-------------|
| 200 | Operación exitosa |
| 201 | Recurso creado |
| 400 | Solicitud incorrecta |
| 404 | Recurso no encontrado |
| 422 | Error de validación |
| 500 | Error interno del servidor |

---

## ☁️ Despliegue en Producción

La API de TechGear está desplegada en **Render**.

- 🌐 **API:** https://taller2-pyfastapi-u0hp.onrender.com/
- 📚 **Swagger UI:** https://taller2-pyfastapi-u0hp.onrender.com/docs

Comando utilizado para iniciar la API:

```bash
uvicorn techgear_api.main:app --host 0.0.0.0 --port $PORT
```

---

## 🌿 Control de Versiones

El proyecto utiliza **Git y GitHub** para controlar y registrar los cambios realizados durante el desarrollo.

Comandos principales:

```bash
git add .
git commit -m "mensaje del commit"
git push origin main
```