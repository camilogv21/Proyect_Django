from django.db import models

# Create your models here.

class Usuario (models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.IntegerField()
    correo = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100)
    clave = models.CharField(max_length=100)
    roles = (
        ("A", "Administrador"),
        ("E", "Empleado"),
        ("C", "Cliente"),
    )
    rol = models.CharField(choices= roles, max_length=1, default="C")
    
    def __str__(self):
        return self.nombre
    
class Mascota (models.Model):
    id_mascota = models.IntegerField()
    nombre_mascota =  models.CharField(max_length=100)
    tipo_mascota = models.CharField(max_length=100)
    edad = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    
class Producto (models.Model):
    codigo_producto = models.IntegerField()
    nombre_producto = models.CharField(max_length=100)
    cantidad= models.IntegerField()
    tipo_producto = models.CharField(max_length=100)
    precio = models.IntegerField()
    
    def __str__(self):
        return f"{self.nombre_producto}"
    
class Servicios (models.Model):
    id_servicio = models.IntegerField()
    nombre_servicio = models.CharField(max_length=100)
    precio_servicio = models.IntegerField()
    
    def __str__(self):
        return self.nombre_servicio
    
class Pago (models.Model):
    id_pago = models.IntegerField()
    medio_pago = models.CharField(max_length=100)
    
    def __str__(self):
        return self.medio_pago
    
class Factura (models.Model):
    id_factura = models.IntegerField()
    nombre_producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField()
    total_sin_descuento = models.IntegerField()
    descuento = models.IntegerField()
    total_con_descuento = models.IntegerField()
    pago = models.ForeignKey(Pago, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    servicios = models.ForeignKey(Servicios, on_delete=models.DO_NOTHING)
    
    def __int__(self):
        return self.id_factura
    
class Citas (models.Model):
    id_cita = models.IntegerField()
    hora_fecha = models.DateTimeField()
    servicio = models.ForeignKey(Servicios, on_delete=models.DO_NOTHING)