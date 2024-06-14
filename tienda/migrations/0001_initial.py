# Generated by Django 4.2.7 on 2024-05-08 16:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nombre', models.CharField(max_length=254)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=254)),
                ('rol', models.IntegerField(choices=[(1, 'Administrador'), (2, 'Despachador'), (3, 'Cliente')], default=3)),
                ('foto', models.ImageField(blank=True, default='fotos/default.png', upload_to='fotos/')),
                ('token_recuperar', models.CharField(blank=True, default='', max_length=254, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=254)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CategoriaEtiqueta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=254, unique=True)),
                ('precio', models.FloatField()),
                ('inventario', models.IntegerField()),
                ('fecha_creacion', models.DateField()),
                ('foto', models.ImageField(default='fotos_productos/default.png', upload_to='fotos_productos/')),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_venta', models.DateTimeField(auto_now=True)),
                ('estado', models.IntegerField(choices=[(1, 'Pendiente'), (2, 'Enviado'), (3, 'Rechazada')], default=1)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategoriaEtiqueta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=254)),
                ('id_categoria_etiqueta', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tienda.categoriaetiqueta')),
            ],
        ),
        migrations.CreateModel(
            name='ProductoSubCategoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tienda.producto')),
                ('id_sub_categoria_etiqueta', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tienda.subcategoriaetiqueta')),
            ],
        ),
        migrations.AddField(
            model_name='producto',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.subcategoriaetiqueta'),
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('precio_historico', models.IntegerField()),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tienda.producto')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tienda.venta')),
            ],
        ),
    ]