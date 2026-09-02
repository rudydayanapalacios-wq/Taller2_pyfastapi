from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),

    path(
        "productos/",
        views.productos,
        name="productos"
    ),

    path(
        "productos/crear/",
        views.crear_producto,
        name="crear_producto"
    ),

    path(
        "productos/editar/<str:producto_id>/",
        views.editar_producto,
        name="editar_producto"
    ),

    path(
        "productos/eliminar/<str:producto_id>/",
        views.eliminar_producto,
        name="eliminar_producto"
    ),

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

        path(
        "pedidos/",
        views.pedidos,
        name="pedidos"
    ),
]