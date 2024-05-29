from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError, transaction
from rest_framework import viewsets 
from .serializers import *
# Para tomar el from desde el settings
from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage
import re
from .crypt import *


# Importamos todos los modelos de la base de datos
from .models import *

# Create your views here.

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
""" class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    """
    
class CategoriaEtiquetaViewSet(viewsets.ModelViewSet):
    queryset = CategoriaEtiqueta.objects.all()
    serializer_class = CategoriaEtiquetaSerializer

class SubCategoriaEtiquetaViewSet(viewsets.ModelViewSet):
    queryset = SubCategoriaEtiqueta.objects.all()
    serializer_class = SubCategoriaEtiquetaSerializer
    
class ProductoSubCategoriaViewSet(viewsets.ModelViewSet):
    queryset = ProductoSubCategoria.objects.all()
    serializer_class = ProductoSubCategoriaSerializer
    
class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    
class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer
    
def index(request):
	logueo = request.session.get("logueo", False)

	if logueo == False:
		return render(request, "tienda/login/login.html")
	else:
		return redirect("inicio")
	
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class CategoriaViewSet(viewsets.ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = Categoria.objects.all()
	serializer_class = CategoriaSerializer


class UsuarioViewSet(viewsets.ModelViewSet):	
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Usuario.objects.all()
	serializer_class = UsuarioSerializer

def registrar_usuario(request):
	if request.method == "POST":
		nombre = request.POST.get("nombre")
		correo = request.POST.get("correo")
		clave1 = request.POST.get("clave1")
		clave2 = request.POST.get("clave2")
		if clave1 == clave2:
			q = Usuario(
				nombre=nombre,
				email=correo,
				password=hash_password(clave1)
			)
			q.save()
			messages.success(request, "Usuario registrado correctamente!!")
			return redirect("index")
		else:
			messages.warning(request, "No concuerdan las contraseñas")
			return redirect("registrar_usuario")
	else:
		return render(request, "tienda/login/registro.html")


def login(request):
	if request.method == "POST":
		user = request.POST.get("email")
		passw = request.POST.get("password")
		# select * from Usuario where correo = "user" and clave = "passw"
		if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", user):
			messages.error(request, f"El correo ingresado no es valido")
		try:
			q = Usuario.objects.get(email=user, password=passw)
			# Crear variable de sesión
			request.session["logueo"] = {
				"id": q.id,
				"nombre": q.nombre,
				"rol": q.rol,
				"nombre_rol": q.get_rol_display()
			}
			request.session["carrito"] = []
			request.session["items"] = 0
			messages.success(request, f"Bienvenido {q.nombre}!!")
			return redirect("inicio")
		except Exception as e:
			messages.error(request, "Error: Usuario o contraseña incorrectos...")
			return redirect("index")
	else:
		messages.warning(request, "Error: No se enviaron datos...")
		return redirect("index")


def logout(request):
	try:
		del request.session["logueo"]
		del request.session["carrito"]
		del request.session["items"]
		messages.success(request, "Sesión cerrada correctamente!")
		return redirect("inicio")
	except Exception as e:
		messages.warning(request, "No se pudo cerrar sesión...")
		return redirect("")


def inicio(request):
	logueo = request.session.get("logueo", False)

	categorias = CategoriaEtiqueta.objects.all()
	count = 0
	etiquetas = []
	for categoria in categorias:
		name = {'nombre': categoria.nombre,
				'subEtiquetas': []
				}
		etiquetas.append(name)
		subcat = SubCategoriaEtiqueta.objects.filter(id_categoria_etiqueta=categoria.id)
		for subcategoria in subcat:
			etiquetas[count]['subEtiquetas'].append(subcategoria)
		count += 1
	cat = request.GET.get("cat")
	if cat == None:
		productos = Producto.objects.all()
	else:
		c = CategoriaEtiqueta.objects.get(pk=cat)
		productos = Producto.objects.filter(categoria=c)
		

	contexto = {"data": productos, "cat": categorias, "etq": etiquetas}
	return render(request, "tienda/inicio/inicio.html", contexto)
	
def recuperar_clave(request):
	if request.method == "POST":
		email = request.POST.get("correo")
		try:
			q = Usuario.objects.get(email=email)
			from random import randint
			import base64
			token = base64.b64encode(str(randint(100000, 999999)).encode("ascii")).decode("ascii")
			print(token)
			q.token_recuperar = token
			q.save()
			# enviar correo de recuperación
			destinatario = email
			mensaje = f"""
					<h1 style='color:blue;'>Tienda virtual</h1>
					<p>Usted ha solicitado recuperar su contraseña, haga clic en el link y digite el token.</p>
					<p>Token: <strong>{token}</strong></p>
					<a href='http://127.0.0.1:8000/tienda/verificar_recuperar/?correo={email}'>Recuperar...</a>
					"""
			try:
				msg = EmailMessage("Tienda ADSO", mensaje, settings.EMAIL_HOST_USER, [destinatario])
				msg.content_subtype = "html"  # Habilitar contenido html
				msg.send()
				messages.success(request, "Correo enviado!!")
			except BadHeaderError:
				messages.error(request, "Encabezado no válido")
			except Exception as e:
				messages.error(request, f"Error: {e}")
			# fin -
		except Usuario.DoesNotExist:
			messages.error(request, "No existe el usuario....")
		return redirect("recuperar_clave")
	else:
		return render(request, "tienda/login/recuperar.html")


def verificar_recuperar(request):
	if request.method == "POST":
		if request.POST.get("check"):
			# caso en el que el token es correcto
			email = request.POST.get("correo")
			q = Usuario.objects.get(email=email)

			c1 = request.POST.get("nueva1")
			c2 = request.POST.get("nueva2")

			if c1 == c2:
				# cambiar clave en DB
				q.password = hash_password(c1)
				q.token_recuperar = ""
				q.save()
				messages.success(request, "Contraseña guardada correctamente!!")
				return redirect("index")
			else:
				messages.info(request, "Las contraseñas nuevas no coinciden...")
				return redirect("verificar_recuperar")+"/?correo="+email
		else:
			# caso en el que se hace clic en el correo-e para digitar token
			email = request.POST.get("correo")
			token = request.POST.get("token")
			q = Usuario.objects.get(email=email)
			if (q.token_recuperar == token) and q.token_recuperar != "":
				contexto = {"check": "ok", "correo":email}
				return render(request, "tienda/login/verificar_recuperar.html", contexto)
			else:
				messages.error(request, "Token incorrecto")
				return redirect("verificar_recuperar")	# falta agregar correo como parametro url
	else:
		correo = request.GET.get("correo")
		contexto = {"correo":correo}
		return render(request, "tienda/login/verificar_recuperar.html", contexto)


from .decorador_especial import *


@login_requerido
def categorias(request):
	q = CategoriaEtiqueta.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/categorias/categorias.html", contexto)



def categorias_form(request):
	return render(request, "tienda/categorias/categorias_form.html")


def categorias_crear(request):
	if request.method == "POST":
		nomb = request.POST.get("nombre")
		if not re.match(r"^[a-zA-Z\s]+$", nomb):
			messages.error(request, f"El nombre solo puede llevar valores alfabeticos")
		try:
			q = CategoriaEtiqueta(
				nombre=nomb,
			)
			q.save()
			messages.success(request, "Guardado correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
		return redirect("categorias_listar")

	else:
		messages.warning(request, "Error: No se enviaron datos...")
		return redirect("categorias_listar")


def categorias_eliminar(request, id):
	try:
		q = CategoriaEtiqueta.objects.get(pk=id)
		q.delete()
		messages.success(request, "Categoría eliminada correctamente!!")
	except Exception as e:
		messages.error(request, f"Error: {e}")

	return redirect("categorias_listar")


def categorias_formulario_editar(request, id):
	q = CategoriaEtiqueta.objects.get(pk=id)
	contexto = {"data": q}
	return render(request, "tienda/categorias/categorias_formulario_editar.html", contexto)

def categorias_actualizar(request):
	if request.method == "POST":
		id = request.POST.get("id")
		nomb = request.POST.get("nombre")
		desc = request.POST.get("descripcion")

		try:
			q = CategoriaEtiqueta.objects.get(pk=id)
			q.nombre = nomb
			q.descripcion = desc
			q.save()
			messages.success(request, "Categoría actualizada correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
	else:
		messages.warning(request, "Error: No se enviaron datos...")

	return redirect("categorias_listar")


@login_requerido
def productos(request):
	q = Producto.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/productos/productos.html", contexto)


def productos_form(request):
	q = CategoriaEtiqueta.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/productos/productos_form.html", contexto)


def productos_crear(request):
	if request.method == "POST":
		nombre = request.POST.get("nombre")
		precio = request.POST.get("precio")
		inventario = request.POST.get("inventario")
		fecha_creacion = request.POST.get("fecha_creacion")
		categoria = SubCategoriaEtiqueta.objects.get(pk=request.POST.get("categoria"))
		if not re.match(r"^[a-zA-Z\s]+$", nombre):
			messages.error(request, f"El nombre solo puede llevar valores alfabeticos")
		if not re.match(r"^\d", precio):
			messages.error(request, f"El precio solo puede llevar valores numericos")
		if not re.match(r"^\d", inventario):
			messages.error(request, f"El inventario solo puede llevar valores numericos")
		try:
			q = Producto(
				nombre=nombre,
				precio=precio,
				inventario=inventario,
				fecha_creacion=fecha_creacion,
				categoria=categoria
			)
			q.save()
			messages.success(request, "Guardado correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: No se enviaron datos...")
		return redirect("productos_listar")

	else:
		messages.warning(request, "Error: No se enviaron datos...")
		return redirect("productos_listar")


def productos_eliminar(request, id):
	try:
		q = Producto.objects.get(pk=id)
		q.delete()
		messages.success(request, "Producto eliminada correctamente!!")
	except Exception as e:
		messages.error(request, f"Error: {e}")

	return redirect("productos_listar")


def productos_formulario_editar(request, id):
	q = Producto.objects.get(pk=id)
	c = CategoriaEtiqueta.objects.all()
	contexto = {"data": q, "categoria": c}
	return render(request, "tienda/productos/productos_formulario_editar.html", contexto)

def productos_actualizar(request):
	if request.method == "POST":
		id = request.POST.get("id")
		nombre = request.POST.get("nombre")
		precio = request.POST.get("precio")
		inventario = request.POST.get("inventario")
		fecha_creacion = request.POST.get("fecha_creacion")
		categoria = CategoriaEtiqueta.objects.get(pk=request.POST.get("categoria"))
		if not re.match(r"^[a-zA-Z\s]+$", nombre):
			messages.error(request, f"El nombre solo puede llevar valores alfabeticos")
		if not re.match(r"^\d", precio):
			messages.error(request, f"El precio solo puede llevar valores numericos")
		if not re.match(r"^\d", inventario):
			messages.error(request, f"El inventario solo puede llevar valores numericos")
		try:
			q = Producto.objects.get(pk=id)
			q.nombre = nombre
			q.precio = precio
			q.inventario = inventario
			q.fecha_creacion = fecha_creacion
			q.categoria = categoria
			q.save()
			messages.success(request, "Producto actualizado correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: No se enviaron datos...")
	else:
		messages.warning(request, "Error: No se enviaron datos...")

	return redirect("productos_listar")


def ver_perfil(request):
	logueo = request.session.get("logueo", False)
	# Consultamos en DB por el ID del usuario logueado....
	q = Usuario.objects.get(pk=logueo["id"])
	contexto = {"data": q}
	return render(request, "tienda/login/perfil.html", contexto)


def cambio_clave_formulario(request):
	return render(request, "tienda/login/cambio_clave.html")


def cambiar_clave(request):
	if request.method == "POST":
		logueo = request.session.get("logueo", False)
		q = Usuario.objects.get(pk=logueo["id"])

		c1 = request.POST.get("nueva1")
		c2 = request.POST.get("nueva2")

		if q.clave == request.POST.get("clave"):
			if c1 == c2:
				# cambiar clave en DB
				q.clave = c1
				q.save()
				messages.success(request, "Contraseña guardada correctamente!!")
			else:
				messages.info(request, "Las contraseñas nuevas no coinciden...")
		else:
			messages.error(request, "Contraseña no válida...")
	else:
		messages.warning(request, "Error: No se enviaron datos...")

	return redirect('cc_formulario')


def carrito_add(request):
	if request.method == "POST":
		try:
			carrito = request.session.get("carrito", False)
			if not carrito:
				request.session["carrito"] = []
				request.session["items"] = 0
				carrito = []

			id_producto = int(request.POST.get("id"))
			cantidad = request.POST.get("cantidad")
			# Consulto el producto en DB...........................
			q = Producto.objects.get(pk=id_producto)
			for p in carrito:
				if p["id"] == id_producto:
					if q.inventario >= (p["cantidad"] + int(cantidad)) and int(cantidad) > 0:
						p["cantidad"] += int(cantidad)
						p["subtotal"] = p["cantidad"] * q.precio
					else:
						print("Cantidad supera inventario...")
						messages.warning(request, "Cantidad supera inventario...")
					break
			else:
				print("No existe en carrito... lo agregamos")
				if q.inventario >= int(cantidad) and int(cantidad) > 0:
					carrito.append(
						{
							"id": q.id,
							"foto": q.foto.url,
							"producto": q.nombre,
							"precio": q.precio,
							"cantidad": int(cantidad),
							"subtotal": int(cantidad) * q.precio
						}
					)
				else:
					print("Cantidad supera inventario...")
					messages.warning(request, "No se puede agregar, no hay suficiente inventario.")

			# Actualizamos variable de sesión carrito...
			request.session["carrito"] = carrito

			contexto = {
				"items": len(carrito),
				"total": sum(p["subtotal"] for p in carrito)
			}
			request.session["items"] = len(carrito)

			return render(request, "tienda/carrito/carrito.html", contexto)
		except ValueError as e:
			messages.error(request, f"Error: Digite un valor correcto para cantidad")
			return HttpResponse("Error")
		except Exception as e:
			messages.error(request, f"Ocurrió un Error: {e}")
			return HttpResponse("Error")
	else:
		messages.warning(request, "No se enviaron datos.")
		return HttpResponse("Error")


def carrito_ver(request):
	carrito = request.session.get("carrito", False)
	if not carrito:
		request.session["carrito"] = []
		request.session["items"] = 0
		contexto = {
			"items": 0,
			"total": 0
		}
	else:
		contexto = {
			"items": len(carrito),
			"total": sum(p["subtotal"] for p in carrito)
		}
		request.session["items"] = len(carrito)

	return render(request, "tienda/carrito/carrito.html", contexto)


def vaciar_carrito(request):
	request.session["carrito"] = []
	request.session["items"] = 0
	return redirect("inicio")


def eliminar_item_carrito(request, id_producto):
	try:
		carrito = request.session.get("carrito", False)
		if carrito != False:
			for i, item in enumerate(carrito):
				if item["id"] == id_producto:
					carrito.pop(i)
					break
			else:
				messages.warning(request, "No se encontró el ítem en el carrito.")

		request.session["items"] = len(carrito)
		request.session["carrito"] = carrito
		return redirect("carrito_ver")
	except:
		return HttpResponse("Error")


def actualizar_totales_carrito(request, id_producto):
	carrito = request.session.get("carrito", False)
	cantidad = request.GET.get("cantidad")

	if carrito != False:
		for i, item in enumerate(carrito):
			if item["id"] == id_producto:
				item["cantidad"] = int(cantidad)
				item["subtotal"] = int(cantidad) * item["precio"]
				break
		else:
			messages.warning(request, "No se encontró el ítem en el carrito.")

	request.session["items"] = len(carrito)
	request.session["carrito"] = carrito
	return redirect("carrito_ver")


def realizar_venta(request):
    try:
        logueo = request.session.get("logueo")
        usuario = Usuario.objects.get(pk=logueo["id"])
        nueva_venta = Venta.objects.create(usuario=usuario)

        carrito = request.session.get("carrito", [])
        for item in carrito:
            producto = Producto.objects.get(pk=item["id"])
            cantidad = item["cantidad"]

            detalle_venta = DetalleVenta.objects.create(
                venta=nueva_venta,
                producto=producto,
                cantidad=cantidad,
                precio_historico=producto.precio
            )

            producto.inventario -= cantidad
            producto.save()

        request.session["carrito"] = []
        request.session["items"] = 0

        messages.success(request, "¡La compra se realizó con éxito!")

    except Producto.DoesNotExist as e:
        messages.error(request, f"Error al procesar la compra: {e}")
    except Exception as e:
        messages.error(request, f"Ocurrió un error al procesar la compra: {e}")

    return redirect("inicio")


@transaction.atomic
def guardar_venta(request):
	carrito = request.session.get("carrito", False)
	logueo = request.session.get("logueo", False)
	try:
		# Genero encabezado de venta, para tener ID y guardar detalle
		r = Venta(usuario=Usuario.objects.get(pk=logueo["id"]))
		r.save()

		for i, p in enumerate(carrito):
			try:
				pro = Producto.objects.get(pk=p["id"])
				print(f"ok producto {p['producto']}")
			except Producto.DoesNotExist:
				# elimino el producto no existente del carrito...
				carrito.pop(i)
				request.session["carrito"] = carrito
				request.session["items"] = len(carrito)
				raise Exception(f"El producto '{p['producto']}' ya no existe")

			if int(p["cantidad"]) > pro.inventario:
				raise Exception(f"La cantidad del producto '{p['producto']}' supera el inventario")

			det = DetalleVenta(
				venta=r,
				producto=pro,
				cantidad=int(p["cantidad"]),
				precio_historico=int(p["precio"])
			)
			det.save()
		messages.success(request, "Venta realizada correctamente!!")
	except Exception as e:
		transaction.set_rollback(True)
		messages.error(request, f"Error: {e}")

	return redirect("inicio")

def prueba_correo(request):
	destinatario = "hammer.hernandez10@gmail.com"
	mensaje = """
		<h1 style='color:blue;'>Tienda virtual</h1>
		<p>Su pedido está listo y en estado "creado".</p>
		<h1 style='color:red;'> ESTA MUY ENAMORADO </h1>
		<p>Tienda ADSO, 2024</p>
		"""
 	
	try:
		msg = EmailMessage("Tienda ADSO", mensaje, settings.EMAIL_HOST_USER, [destinatario])
		msg.content_subtype = "html"  # Habilitar contenido html
		msg.send()
		return HttpResponse("Correo enviado")
	except BadHeaderError:
		return HttpResponse("Encabezado no válido")
	except Exception as e:
		return HttpResponse(f"Error: {e}")
	




def etiquetas_listar(request):
	q = SubCategoriaEtiqueta.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/categorias/subcategoria/etiquetas.html", contexto)

def etiquetas_form(request):
	q = CategoriaEtiqueta.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/categorias/subcategoria/etiquetas_form_crear.html", contexto)

def etiquetas_crear(request):
	if request.method == "POST":
		nomb = request.POST.get("nombre")
		cat = CategoriaEtiqueta(pk=request.POST.get("categoriaEtiqueta"))
		if not re.match(r"^[a-zA-Z\s]+$", nomb):
			messages.error(request, f"El nombre solo puede llevar valores alfabeticos")
		try:
			q = SubCategoriaEtiqueta(
				nombre=nomb,
				id_categoria_etiqueta=cat
			)
			q.save()
			messages.success(request, "Guardado correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: No se enviaron los datos...")
		return redirect("etiquetas_listar")

	else:
		messages.warning(request, "Error: No se enviaron datos...")
		return redirect("etiquetas_listar")

def etiquetas_eliminar(request, id):
	try:
		q = SubCategoriaEtiqueta.objects.get(pk=id)
		q.delete()
		messages.success(request, "Etiqueta eliminada correctamente!!")
	except Exception as e:
		messages.error(request, f"Error: {e}")

	return redirect("etiquetas_listar")

def etiquetas_formulario_editar(request, id):
	q = SubCategoriaEtiqueta.objects.get(pk=id)
	c = CategoriaEtiqueta.objects.all()
	contexto = {"data": q, "categorias": c}
	return render(request, "tienda/categorias/subcategoria/etiquetas_form_editar.html", contexto)

def etiquetas_actualizar(request):
	if request.method == "POST":
		id = request.POST.get("id")
		nomb = request.POST.get("nombre")
		cat = CategoriaEtiqueta.objects.get(pk=request.POST.get("categoriaEtiqueta"))
		if not re.match(r"^[a-zA-Z\s]+$", nomb):
			messages.error(request, f"El nombre solo puede llevar valores alfabeticos")
		try:
			q = SubCategoriaEtiqueta.objects.get(pk=id)
			q.nombre = nomb
			q.id_categoria_etiqueta = cat
			q.save()
			messages.success(request, "Etiqueta actualizada correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
	else:
		messages.warning(request, "Error: No se enviaron datos...")

	return redirect("etiquetas_listar")
