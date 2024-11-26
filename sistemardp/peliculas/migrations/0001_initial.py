# Generated by Django 5.1.3 on 2024-11-26 23:26

import django.db.models.deletion
import peliculas.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaPel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreCatPel', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Categoria de Pelicula',
                'verbose_name_plural': 'Categorias de Peliculas',
            },
        ),
        migrations.CreateModel(
            name='pelicula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(help_text='nombre de la pelicula', max_length=25)),
                ('imagen', models.ImageField(blank=True, help_text='Imagen del producto frontal', null=True, upload_to=peliculas.models.upload_to)),
                ('precio', models.DecimalField(decimal_places=2, help_text='Precio de la pelicula', max_digits=5)),
                ('descuento', models.IntegerField(default=0, help_text='Descuento')),
                ('publicacion', models.DateField(help_text='año en que se publico la pelicula')),
                ('calificacion', models.IntegerField(help_text='calificacion de la pelicula')),
                ('stock', models.PositiveIntegerField(help_text='cantidad disponible en stock')),
                ('descripcion', models.TextField(help_text='descripcion de la pelicula', max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('categorias', models.ForeignKey(help_text='categorias de la pelicula', on_delete=django.db.models.deletion.CASCADE, to='peliculas.categoriapel')),
            ],
            options={
                'verbose_name': 'Pelicula',
                'verbose_name_plural': 'Peliculas',
            },
        ),
    ]
