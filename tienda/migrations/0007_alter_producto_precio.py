# Generated by Django 4.2.6 on 2024-02-07 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0006_producto_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.FloatField(),
        ),
    ]
