import requests

from django.shortcuts import render, redirect


API_URL = "http://127.0.0.1:8001"


def inicio(request):
    return render(request, "catalogo/inicio.html")



def productos(request):
    url = f"{API_URL}/productos/"

    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        productos = respuesta.json()

    except requests.RequestException as error:
        productos = []
        print(f"Error al conectar con FastAPI: {error}")

    return render(
        request,
        "catalogo/productos.html",
        {
            "productos": productos
        }
    )


def crear_producto(request):

    if request.method == "POST":

        datos_producto = {
            "nombre": request.POST.get("nombre"),
            "descripcion": request.POST.get("descripcion"),
            "precio": request.POST.get("precio"),
            "stock": request.POST.get("stock"),
            "categoria": request.POST.get("categoria")
        }

        archivo_imagen = request.FILES.get("imagen")

        files = None

        if archivo_imagen:
            files = {
                "imagen": (
                    archivo_imagen.name,
                    archivo_imagen.file,
                    archivo_imagen.content_type
                )
            }

        url = f"{API_URL}/productos/"

        try:

            if files:

                respuesta = requests.post(
                    url,
                    data=datos_producto,
                    files=files
                )

            else:

                respuesta = requests.post(
                    url,
                    data=datos_producto
                )

            print("STATUS CREAR:", respuesta.status_code)
            print("RESPUESTA CREAR:", respuesta.text)

            respuesta.raise_for_status()

            return redirect("productos")

        except requests.RequestException as error:

            print(f"Error al crear producto: {error}")

            return render(
                request,
                "catalogo/crear_producto.html",
                {
                    "error": "No se pudo crear el producto.",
                    "producto": datos_producto
                }
            )

    return render(
        request,
        "catalogo/crear_producto.html"
    )


def editar_producto(request, producto_id):

    url = f"{API_URL}/productos/{producto_id}"

    if request.method == "GET":

        try:

            respuesta = requests.get(url)

            print("ID PRODUCTO:", producto_id)
            print("STATUS FASTAPI:", respuesta.status_code)
            print("RESPUESTA FASTAPI:", respuesta.text)

            respuesta.raise_for_status()

            producto = respuesta.json()

            return render(
                request,
                "catalogo/editar_producto.html",
                {
                    "producto": producto
                }
            )

        except requests.RequestException as error:

            print(f"Error al obtener producto: {error}")

            return redirect("productos")


    if request.method == "POST":

        datos_producto = {
            "nombre": request.POST.get("nombre"),
            "descripcion": request.POST.get("descripcion"),
            "precio": request.POST.get("precio"),
            "stock": request.POST.get("stock"),
            "categoria": request.POST.get("categoria")
        }

        archivo_imagen = request.FILES.get("imagen")

        files = None

        if archivo_imagen:

            files = {
                "imagen": (
                    archivo_imagen.name,
                    archivo_imagen.file,
                    archivo_imagen.content_type
                )
            }

        try:

            if files:

                respuesta = requests.put(
                    url,
                    data=datos_producto,
                    files=files
                )

            else:

                respuesta = requests.put(
                    url,
                    data=datos_producto
                )

            print("STATUS ACTUALIZAR:", respuesta.status_code)
            print("RESPUESTA ACTUALIZAR:", respuesta.text)

            respuesta.raise_for_status()

            return redirect("productos")

        except requests.RequestException as error:

            print(f"Error al actualizar producto: {error}")

            return render(
                request,
                "catalogo/editar_producto.html",
                {
                    "producto": datos_producto,
                    "error": "No se pudo actualizar el producto."
                }
            )

    return redirect("productos")


def eliminar_producto(request, producto_id):

    if request.method == "POST":

        try:

            respuesta = requests.delete(
                f"{API_URL}/productos/{producto_id}"
            )

            print(
                "STATUS ELIMINAR:",
                respuesta.status_code
            )

            respuesta.raise_for_status()

        except requests.RequestException as error:

            print(
                f"Error al eliminar producto: {error}"
            )

    return redirect("productos")


def checkout(request):

    url_productos = f"{API_URL}/productos/"

    try:

        respuesta = requests.get(url_productos)

        respuesta.raise_for_status()

        productos = respuesta.json()

    except requests.RequestException as error:

        productos = []

        print(
            f"Error al conectar con FastAPI: {error}"
        )

    producto_seleccionado = request.GET.get(
        "producto_id",
        ""
    )

    if request.method == "POST":

        datos_pedido = {
            "cliente": request.POST.get("cliente"),
            "producto_id": request.POST.get("producto_id"),
            "cantidad": int(
                request.POST.get("cantidad")
            ),
            "total": float(
                request.POST.get("total")
            )
        }

        url_pedidos = f"{API_URL}/pedidos/"

        try:

            respuesta = requests.post(
                url_pedidos,
                json=datos_pedido
            )

            respuesta.raise_for_status()

            pedido = respuesta.json()

            return render(
                request,
                "catalogo/checkout.html",
                {
                    "productos": productos,
                    "pedido": pedido
                }
            )

        except requests.RequestException as error:

            print(
                f"Error al crear el pedido: {error}"
            )

            return render(
                request,
                "catalogo/checkout.html",
                {
                    "productos": productos,
                    "producto_seleccionado": producto_seleccionado,
                    "error": "No se pudo crear el pedido."
                }
            )

    return render(
        request,
        "catalogo/checkout.html",
        {
            "productos": productos,
            "producto_seleccionado": producto_seleccionado
        }
    )