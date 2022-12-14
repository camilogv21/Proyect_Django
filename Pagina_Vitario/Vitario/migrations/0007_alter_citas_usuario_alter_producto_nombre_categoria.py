# Generated by Django 4.1.1 on 2022-10-19 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Vitario', '0006_categoria_remove_producto_tipo_producto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citas',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Vitario.usuario'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='nombre_categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Vitario.categoria'),
        ),
    ]
