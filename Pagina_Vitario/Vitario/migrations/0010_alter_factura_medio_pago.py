# Generated by Django 4.1.1 on 2022-10-20 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vitario', '0009_alter_factura_medio_pago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='medio_pago',
            field=models.CharField(choices=[('E', 'Efectivo'), ('T', 'Trasnferencia'), ('A', 'Tarjeta')], default='E', max_length=1),
        ),
    ]
