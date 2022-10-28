# Generated by Django 4.1.1 on 2022-10-20 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vitario', '0007_alter_citas_usuario_alter_producto_nombre_categoria'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categoria',
            old_name='id_categoria',
            new_name='codigo_categoria',
        ),
        migrations.RenameField(
            model_name='servicios',
            old_name='id_servicio',
            new_name='codigo_servicio',
        ),
        migrations.RemoveField(
            model_name='citas',
            name='id_cita',
        ),
        migrations.RemoveField(
            model_name='factura',
            name='id_factura',
        ),
        migrations.RemoveField(
            model_name='factura',
            name='pago',
        ),
        migrations.RemoveField(
            model_name='mascota',
            name='id_mascota',
        ),
        migrations.AddField(
            model_name='factura',
            name='medio_pago',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='Pago',
        ),
    ]
