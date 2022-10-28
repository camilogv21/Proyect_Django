from email.policy import default
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
    foto = models.ImageField(upload_to = 'vitario/fotos', default = 'vitario/fotos/defaultUsu.png')
    
    def __str__(self):
        return self.nombre
    
class Mascota (models.Model):
    nombre_mascota =  models.CharField(max_length=100)
    tipo_mascota = models.CharField(max_length=100)
    edad = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

    
class Producto (models.Model):
    codigo_producto = models.IntegerField()
    nombre_producto = models.CharField(max_length=100)
    cantidad= models.IntegerField()
    precio = models.IntegerField()
    categorias = (
        ("M","Medicamentos"),
        ("A","Accesorios"),
        ("C","Concentrado"),
        ("AP","Alimentos y Premios"),
    )
    categoria = models.CharField(choices=  categorias, max_length=2)
    foto = models.ImageField(upload_to = 'vitario/fotos', default = 'vitario/fotos/defaultPro.png')

    
    def __str__(self):
        return f"{self.nombre_producto}"
    
class Servicios (models.Model):
    codigo_servicio = models.IntegerField()
    nombre_servicio = models.CharField(max_length=100)
    precio_servicio = models.IntegerField()
    foto = models.ImageField(upload_to = 'vitario/fotos', default = 'vitario/fotos/defaultMas.png')  
    
    def __str__(self):
        return self.nombre_servicio
    
class Factura (models.Model):
    nombre_producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField()
    total_sin_descuento = models.IntegerField()
    descuento = models.IntegerField()
    total_con_descuento = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    servicios = models.ForeignKey(Servicios, on_delete=models.DO_NOTHING, default = "Sin servicio")
    pagos = (
        ("E", "Efectivo"),
        ("T", "Trasnferencia"),
        ("A", "Tarjeta"),
    )
    medio_pago = models.CharField(choices=  pagos, max_length=1, default="E")
    
    
class Citas (models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    hora_fecha = models.DateTimeField()
    servicio = models.ForeignKey(Servicios, on_delete=models.DO_NOTHING)