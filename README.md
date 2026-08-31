# ⚡ TECHGEAR

> **Tecnología que impulsa tu mundo.**

**TechGear** es una plataforma web para explorar productos tecnológicos y gestionar pedidos. Está construida con **Django, FastAPI y MongoDB Atlas**, separando el portal web de la lógica de la API REST.

---

## ✦ Sobre TechGear

La plataforma permite consultar un catálogo de productos con:

* **Nombre**
* **Descripción**
* **Categoría**
* **Precio**
* **Stock**

También permite gestionar productos, realizar pedidos y verificar la disponibilidad de stock antes de registrar una compra.

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

* **Django** presenta el catálogo y la interfaz web.
* **FastAPI** gestiona productos, pedidos y validaciones.
* **MongoDB Atlas** almacena la información de forma persistente.
* **Requests** permite la comunicación HTTP entre Django y FastAPI.

---

## 🛠️ Tecnologías

| Tecnología            | Función                                       |
| --------------------- | --------------------------------------------- |
| 🐍 **Python**         | Lenguaje principal                            |
| ⚡ **FastAPI**         | API REST y lógica de negocio                  |
| 🌐 **Django**         | Portal web e interfaz de usuario              |
| 🗄️ **MongoDB Atlas** | Base de datos NoSQL                           |
| 📋 **Pydantic**       | Validación de datos y esquemas                |
| 🔗 **Requests**       | Comunicación HTTP entre Django y FastAPI      |
| 🎨 **HTML / CSS**     | Diseño de interfaz                            |
| 📚 **Swagger UI**     | Documentación interactiva de la API           |
| ☁️ **Render**         | Despliegue de la API                          |
| ▲ **Vercel**          | Configuración de despliegue del portal Django |
| 🐙 **Git / GitHub**   | Control de versiones                          |

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
│   ├── imagenes/
│   ├── database.py
│   └── main.py
│
├── techgear_web/
│   ├── catalogo/
│   │   ├── static/
│   │   │   └── catalogo/
│   │   │       ├── css/
│   │   │       │   ├── inicio.css
│   │   │       │   ├── productos.css
│   │   │       │   └── productos-form.css
│   │   │       └── imagenes/
│   │   │
│   │   ├── templates/
│   │   │   └── catalogo/
│   │   │       ├── inicio.html
│   │   │       ├── productos.html
│   │   │       ├── crear_producto.html
│   │   │       ├── editar_producto.html
│   │   │       └── checkout.html
│   │   │
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── techgear/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   └── manage.py
│
├── build_files.sh
├── vercel.json
├── requirements.txt
├── .gitignore
└── README.md
```

> ⚠️ `database_ambiente502.py` existe físicamente como archivo antiguo/de respaldo, pero la configuración actual utiliza `database.py`.

No se incluyen `venv/`, `.env`, `__pycache__/` ni archivos `.pyc`, ya que no forman parte del código principal del proyecto.

---

## 🌐 Accesos

### ⚡ API en producción

[🚀 TechGear API](https://taller2-pyfastapi-u0hp.onrender.com/?utm_source=chatgpt.com)

### 📚 Swagger UI

[📖 Documentación de la API](https://taller2-pyfastapi-u0hp.onrender.com/docs?utm_source=chatgpt.com)

### 🐙 GitHub

[🔗 Repositorio de TechGear](https://github.com/rudydayanapalacios-wq/Taller2_pyfastapi?utm_source=chatgpt.com)

---

## ⚙️ Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/rudydayanapalacios-wq/Taller2_pyfastapi.git
cd Taller2_pyfastapi
```

### 2. Crear el entorno virtual

En PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Variables de entorno

Configurar las variables necesarias para MongoDB Atlas en un archivo `.env`.

> 🔐 El archivo `.env` contiene información privada y no debe publicarse ni subirse al repositorio.

---

## 💻 Ejecución Local

Django y FastAPI deben ejecutarse simultáneamente en terminales separadas.

### ⚡ FastAPI

Desde la raíz del proyecto:

```bash
uvicorn techgear_api.main:app --reload --port 8001
```

* **API:** http://127.0.0.1:8001/
* **Swagger UI:** http://127.0.0.1:8001/docs

### 🌐 Django

En otra terminal:

```bash
cd techgear_web
python manage.py runserver 8000
```

* **Portal:** http://127.0.0.1:8000/
* **Catálogo:** http://127.0.0.1:8000/productos/

Django utiliza la API ubicada en:

```text
http://127.0.0.1:8001
```

---

## 🔄 Flujo de Integración

```text
Django (Portal Web)
       │
       │ Petición HTTP
       │ requests
       ▼
FastAPI (REST API)
       │
       │ Consulta / Persistencia
       ▼
MongoDB Atlas
       │
       ▼
FastAPI
       │
       ▼
Django → Muestra información al usuario
```

Django obtiene los productos desde FastAPI mediante peticiones HTTP utilizando la librería `requests`.

---

## 🌐 Integración Django y FastAPI

### Django se encarga de:

* Renderizar la interfaz mediante Templates.
* Mostrar dinámicamente los productos obtenidos desde FastAPI.
* Gestionar las rutas y vistas del portal.
* Consultar, crear, editar y eliminar productos.
* Enviar los datos de los pedidos hacia FastAPI.
* Gestionar los errores de comunicación con la API.

### FastAPI se encarga de:

* Procesar las solicitudes recibidas.
* Validar los datos mediante Pydantic.
* Gestionar productos y pedidos.
* Verificar la disponibilidad de stock.
* Comunicarse con MongoDB Atlas.

La comunicación entre ambas aplicaciones se realiza mediante endpoints REST y respuestas en formato JSON.

---

## 📡 Endpoints Principales

| Operación           | Método HTTP | Endpoint          |
| ------------------- | ----------- | ----------------- |
| Consultar productos | GET         | `/productos/`     |
| Crear producto      | POST        | `/productos/`     |
| Consultar producto  | GET         | `/productos/{id}` |
| Editar producto     | PUT         | `/productos/{id}` |
| Eliminar producto   | DELETE      | `/productos/{id}` |
| Crear pedido        | POST        | `/pedidos/`       |
| Consultar pedidos   | GET         | `/pedidos/`       |
| Consultar pedido    | GET         | `/pedidos/{id}`   |
| Actualizar pedido   | PUT         | `/pedidos/{id}`   |
| Eliminar pedido     | DELETE      | `/pedidos/{id}`   |

---

## 🛡️ Validaciones y Manejo de Excepciones

TechGear implementa validaciones y manejo de errores tanto en FastAPI como en Django.

### FastAPI

Se controlan situaciones como:

* ID de producto inválido.
* Producto no encontrado.
* ID de pedido inválido.
* Pedido no encontrado.
* Stock insuficiente.
* Errores de validación de datos.

Cuando un pedido solicita una cantidad superior al stock disponible, la API rechaza la operación.

```json
{
  "detail": "Stock insuficiente"
}
```

### Django

Django captura errores de comunicación mediante `requests.RequestException`.

Si FastAPI no está disponible, el portal puede manejar el error sin detener completamente la aplicación.

---

## 📋 Respuestas HTTP

| Código | Significado                |
| ------ | -------------------------- |
| 200    | Operación exitosa          |
| 201    | Recurso creado             |
| 400    | Solicitud incorrecta       |
| 404    | Recurso no encontrado      |
| 422    | Error de validación        |
| 500    | Error interno del servidor |

---

## 🧪 Flujo de Uso

1. Abrir el portal web.
2. Consultar el catálogo de productos.
3. Crear un producto.
4. Comprobar que aparece en el catálogo.
5. Editar el producto.
6. Realizar un pedido.
7. Comprobar que el stock disminuye.
8. Intentar realizar un pedido con una cantidad superior al stock disponible.
9. Comprobar la respuesta de stock insuficiente.
10. Consultar la documentación Swagger.
11. Comprobar la comunicación entre Django y FastAPI.

---

## ☁️ Despliegue

### FastAPI en Render

La API está desplegada en Render.

* **API:** https://taller2-pyfastapi-u0hp.onrender.com/
* **Swagger:** https://taller2-pyfastapi-u0hp.onrender.com/docs

Comando utilizado para iniciar FastAPI:

```bash
uvicorn techgear_api.main:app --host 0.0.0.0 --port $PORT
```

### Django en Vercel

El proyecto incluye configuración para el despliegue del portal Django mediante Vercel.

Los archivos relacionados con esta configuración son:

```text
vercel.json
wsgi.py
build_files.sh
```

* **`vercel.json`** define la configuración de construcción y las rutas.
* **`wsgi.py`** proporciona el punto de entrada WSGI de Django.
* **`build_files.sh`** contiene las instrucciones utilizadas durante el proceso de construcción.

---

## 🌿 Control de Versiones

El proyecto utiliza **Git y GitHub** para controlar y registrar los cambios realizados durante el desarrollo.

```bash
git add .
git commit -m "mensaje del commit"
git push origin main
```

### Versión actual

```text
v1.0
```

---

## 👤 Autor

TechGear
