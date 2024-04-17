from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name="index"),
	path('inicio/', views.inicio, name="inicio"),

	# Autenticación de usuarios del sistema
	path('login/', views.login, name="login"),
	path('logout/', views.logout, name="logout"),


	# CRUD de Categorías
	path("categorias_listar/", views.categorias, name="categorias_listar"),
	path("categorias_form/", views.categorias_form, name="categorias_form"),
	path("categorias_crear/", views.categorias_crear, name="categorias_crear"),
	path("categorias_eliminar/<int:id>", views.categorias_eliminar, name="categorias_eliminar"),
	path("categorias_formulario_editar/<int:id>", views.categorias_formulario_editar, name="categorias_formulario_editar"),
	path("categorias_actualizar/", views.categorias_actualizar, name="categorias_actualizar"),

	# CRUD de Productos
	path("productos_listar/", views.productos, name="productos_listar"),
	path("productos_form/", views.productos_form, name="productos_form"),
	path("productos_crear/", views.productos_crear, name="productos_crear"),
	path("productos_eliminar/<int:id>", views.productos_eliminar, name="productos_eliminar"),
	path("productos_formulario_editar/<int:id>", views.productos_formulario_editar, name="productos_formulario_editar"),
	path("productos_actualizar/", views.productos_actualizar, name="productos_actualizar"),

	path("ver_perfil/", views.ver_perfil, name="ver_perfil"),
	path("cc_formulario/", views.cambio_clave_formulario, name="cc_formulario"),
	path("cambiar_clave/", views.cambiar_clave, name="cambiar_clave"),

	# carrito de compra
	path("carrito_add/", views.carrito_add, name="carrito_add"),
	path("carrito_ver/", views.carrito_ver, name="carrito_ver"),
	path("vaciar_carrito/", views.vaciar_carrito, name="vaciar_carrito"),
	path("eliminar_item_carrito/<int:id_producto>", views.eliminar_item_carrito, name="eliminar_item_carrito"),
	path("actualizar_totales_carrito/<int:id_producto>/", views.actualizar_totales_carrito, name="actualizar_totales_carrito"),
 
	#ventas
	path("realizar_venta/", views.realizar_venta, name="realizar_venta"),
	path("prueba_correo/", views.prueba_correo, name="prueba_correo"),
    

	#etiquetas
    path("etiquetas_listar/", views.etiquetas_listar, name="etiquetas_listar"),
    path("etiquetas_crear/", views.etiquetas_crear, name="etiquetas_crear"),
    path("etiquetas_eliminar/<int:id>", views.etiquetas_eliminar, name="etiquetas_eliminar"),
    path("etiquetas_form_editar/<int:id>", views.etiquetas_formulario_editar, name="etiquetas_form_editar"),
    path("etiquetas_actualizar", views.etiquetas_actualizar, name="etiquetas_actualizar"),
    path("etiquetas_form/", views.etiquetas_form, name="etiquetas_form"),

]
