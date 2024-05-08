from django.contrib.auth.models import AbstractUser
from .authentication import CustomUserManager

from django.db import models

# Create your models here.

class Usuario(AbstractUser):
	username = None
	nombre = models.CharField(max_length=254)
	email = models.EmailField(max_length=254, unique=True)
	password = models.CharField(max_length=254)
	ROLES = (
		(1, "Administrador"),
		(2, "Despachador"),
		(3, "Cliente"),
	)
	rol = models.IntegerField(choices=ROLES, default=3)
	foto = models.ImageField(upload_to="fotos/", default="fotos/default.png", blank=True)
	token_recuperar = models.CharField(max_length=254, default="", blank=True, null=True)
	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["nombre"]
	objects = CustomUserManager()

	def __str__(self):
		return self.nombre

class Categoria(models.Model):
	nombre = models.CharField(max_length=254)
	descripcion = models.TextField()

	def __str__(self):
		return self.nombre


class CategoriaEtiqueta(models.Model):
	nombre = models.CharField(max_length=254, unique=True)

	def __str__(self):
		return self.nombre
	
	
class SubCategoriaEtiqueta(models.Model):
	nombre = models.CharField(max_length=254)
	id_categoria_etiqueta = models.ForeignKey(CategoriaEtiqueta, on_delete=models.DO_NOTHING)

	def __str__(self):
		return self.nombre
	

class Producto(models.Model):
	nombre = models.CharField(max_length=254, unique=True)
	precio = models.FloatField()
	inventario = models.IntegerField()
	fecha_creacion = models.DateField()
	categoria = models.ForeignKey(SubCategoriaEtiqueta, on_delete=models.CASCADE )
	foto = models.ImageField(upload_to="fotos_productos/", default="fotos_productos/default.png")

	def __str__(self):
		return self.nombre





class ProductoSubCategoria(models.Model):
	id_producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
	id_sub_categoria_etiqueta = models.ForeignKey(SubCategoriaEtiqueta, on_delete=models.DO_NOTHING)

	def __str__(self):
		return self.id_producto
	


class Venta(models.Model):
	fecha_venta = models.DateTimeField(auto_now=True)
	usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
	ESTADOS = (
		(1, 'Pendiente'),
		(2, 'Enviado'),
		(3, 'Rechazada'),
	)
	estado = models.IntegerField(choices=ESTADOS, default=1)

	def __str__(self):
		return f"{self.id} - {self.usuario}"


class DetalleVenta(models.Model):
	venta = models.ForeignKey(Venta, on_delete=models.DO_NOTHING)
	producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
	cantidad = models.IntegerField()
	precio_historico = models.IntegerField()

	def __str__(self):
		return f"{self.id} - {self.venta}"

