import requests
from django.shortcuts import render


def inicio(request):
    return render(request, "catalogo/inicio.html")


def productos(request):
    url = "http://127.0.0.1:8000/productos"

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
        {"productos": productos}
    )