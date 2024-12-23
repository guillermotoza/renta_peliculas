# Generated by Django 5.1.3 on 2024-12-05 00:39

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
                ('id', models.AutoField(primary_key=True, serialize=False)),
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
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(help_text='nombre de la pelicula', max_length=25)),
                ('imagen', models.ImageField(blank=True, help_text='Imagen del poster de pelicula', null=True, upload_to='peliculas')),
                ('banner', models.ImageField(blank=True, help_text=' imagen de fondo para la pagina de detalles de la pelicula', null=True, upload_to='peliculas/banners')),
                ('precio', models.DecimalField(decimal_places=2, help_text='Precio de la pelicula', max_digits=5)),
                ('descuento', models.IntegerField(default=0, help_text='Descuento en porcentaje')),
                ('publicacion', models.DateField(help_text='año en que se publico la pelicula')),
                ('calificacion', models.IntegerField(help_text='calificacion de la pelicula')),
                ('stock', models.PositiveIntegerField(help_text='cantidad disponible en stock')),
                ('descripcion', models.TextField(help_text='descripcion de la pelicula', max_length=200)),
                ('director', models.CharField(default='Desconocido', max_length=100)),
                ('trailer', models.TextField(default='trailer no disponible', help_text='codigo de insertar de youtube', max_length=1000, validators=[peliculas.models.validar_trailer])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('categorias', models.ManyToManyField(help_text='categorias de la pelicula', to='peliculas.categoriapel')),
            ],
            options={
                'verbose_name': 'Pelicula',
                'verbose_name_plural': 'Peliculas',
            },
        ),
    ]
