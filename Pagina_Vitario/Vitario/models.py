from email.policy import default
from django.db import models

""" Crea una clase llamada Usuario, que es un modelo y esta conectada con otras clases
    La función __str__ es una función especial que se llama cuando imprime un objeto
    :return: El nombre del objeto
"""

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
    
"""Crea una clase llamada Mascota que tiene un nombre, tipo, edad y usuario.
"""
class Mascota (models.Model):
    nombre_mascota =  models.CharField(max_length=100)
    tipo_mascota = models.CharField(max_length=100)
    edad = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    
"""Crea una clase llamada Producto que tiene los siguientes atributos: codigo_producto,
    nombre_producto, cantidad, precio, categorias, categoria, and foto.
    return: el monbre del producto
"""
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
        return f"{self.nombre_producto}-{self.precio}"
    
"""Crea una clase llamada Servicios que tiene el codigo, el nombre y el precio.
    return: el nombre del servicio
"""
class Servicios (models.Model):
    codigo_servicio = models.IntegerField()
    nombre_servicio = models.CharField(max_length=100)
    precio_servicio = models.IntegerField()
    foto = models.ImageField(upload_to = 'vitario/fotos', default = 'vitario/fotos/defaultMas.png')  
    
    def __str__(self):
        return self.nombre_servicio
    
"""Crea una clase llamada Factura, que es un modelo.
"""
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
    medio_pago = models.CharField(choices=pagos, max_length=1, default="E")

class Disponibilidad(models.Model):
    empleado = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    DIAS = (
        ('L', 'Lunes'),
        ('M', 'Martes'),
        ('X', 'Miércoles'),
        ('J', 'Jueves'),
        ('V', 'Viernes'),
        ('S', 'Sábado'),
        ('D', 'Domingo'),
    )
    dia = models.CharField(max_length=1, choices=DIAS)
    HORAS = (
        (9, '9AM'),
        (10, '10AM'),
        (11, '11AM'),
        (12, '12M'),
        (13, '1PM'),
        (14, '2PM'),
        (15, '3PM'),
        (16, '4PM'),
        (17, '5PM'),
        (18, '6PM'),
        (19, '7PM'),
        (20, '8PM'),
    )
    hora = models.IntegerField(choices=HORAS)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    reservado = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.id} - {self.empleado}"
    
"""Citas es un modelo que tiene una clave externa para el usuario, un DateTimeField y una clave externa para los servicios.
"""
class Citas (models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    disponibilidad= models.ForeignKey(Disponibilidad, on_delete=models.DO_NOTHING)
    ESTADO = (
        (1, 'Reservado'),
        (2, 'Cumplida'),
        (3, 'Cancelada'),
    )
    estado = models.IntegerField(choices=ESTADO)
