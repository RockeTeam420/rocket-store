from rest_framework import  serializers
from .models import *

# Serializers define the API representation.
class CategoriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']


class ProductoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'inventario', 'categoria', 'foto']

    
class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'correo','clave', 'ROLES', 'rol', 'foto']

class CategoriaEtiquetaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CategoriaEtiqueta
        fields = ['id', 'nombre']

class SubCategoriaEtiquetaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubCategoriaEtiqueta
        fields = ['id', 'nombre', 'id_categoria_etiqueta']

class ProductoSubCategoriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductoSubCategoria
        fields = ['id', 'id_producto', 'id_sub_categoria_etiqueta']


class VentaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Venta
        fields = ['id', 'fecha_venta', 'usuario', 'ESTADOS', 'estado']

class DetalleVentaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = ['id', 'venta', 'producto', 'cantidad', 'precio_historico']
