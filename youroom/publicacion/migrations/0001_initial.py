# Generated by Django 2.2.18 on 2021-04-30 13:47

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='publicaciones/')),
                ('descripcion', models.TextField(null=True, verbose_name='Descripcion')),
                ('fecha_publicacion', models.DateTimeField(auto_now_add=True)),
                ('categoria', models.CharField(max_length=250)),
                ('totalValoraciones', models.BigIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.UsuarioPerfil')),
            ],
        ),
        migrations.CreateModel(
            name='Destacada',
            fields=[
                ('es_destacada', models.BooleanField(verbose_name='Es destacada')),
                ('fecha_destacada', models.DateTimeField(auto_now_add=True, verbose_name='Fecha destacada')),
                ('publicacion', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='publicacion.Publicacion')),
            ],
        ),
        migrations.CreateModel(
            name='Etiqueta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=10)),
                ('enlace', models.TextField()),
                ('coord_x', models.FloatField()),
                ('coord_y', models.FloatField()),
                ('publicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publicacion.Publicacion')),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('publicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publicacion.Publicacion')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.UsuarioPerfil')),
            ],
            options={
                'ordering': ['-fecha'],
            },
        ),
    ]
