# Generated by Django 3.2.12 on 2022-12-07 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Vitario', '0014_alter_producto_categoria'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='citas',
            name='hora_fecha',
        ),
        migrations.RemoveField(
            model_name='citas',
            name='servicio',
        ),
        migrations.AddField(
            model_name='citas',
            name='estado',
            field=models.IntegerField(choices=[(1, 'Reservado'), (2, 'Cumplida'), (3, 'Cancelada')], default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Disponibilidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.CharField(choices=[('L', 'Lunes'), ('M', 'Martes'), ('X', 'Miércoles'), ('J', 'Jueves'), ('V', 'Viernes'), ('S', 'Sábado'), ('D', 'Domingo')], max_length=1)),
                ('hora', models.IntegerField(choices=[(9, '9AM'), (10, '10AM'), (11, '11AM'), (12, '12M'), (13, '1PM'), (14, '2PM'), (15, '3PM'), (16, '4PM'), (17, '5PM'), (18, '6PM'), (19, '7PM'), (20, '8PM')])),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('reservado', models.BooleanField(default=False)),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Vitario.servicios')),
            ],
        ),
        migrations.AddField(
            model_name='citas',
            name='disponibilidad',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='Vitario.disponibilidad'),
            preserve_default=False,
        ),
    ]
