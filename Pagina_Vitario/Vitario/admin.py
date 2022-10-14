from django.contrib import admin
from .models import Usuario, Mascota, Pago, Producto, Factura, Servicios, Citas

# Register your models here.

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ( 'nombre', 'direccion', 'telefono', 'correo', 'usuario', 'clave', 'rol')
    search_fields = [ 'nombre','rol']
    
@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('id_mascota', 'nombre_mascota', 'tipo_mascota', 'edad', 'usuario', )
    search_fields = ['nombre_mascota', 'usuario']
    
    def edad(self, obj):
        from datetime import date
        hoy = date.today()
        
        edad = hoy.year - obj.fecha_nacimiento.year - ((hoy.month,hoy.day)<(obj.fecha_nacimiento.month, obj.fecha_nacimiento.day))
        return edad
    
@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id_pago', 'medio_pago', )
    
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo_producto', 'nombre_producto', 'cantidad', 'tipo_producto', 'precio', )
    search_fields = ['id_producto', 'nombre_producto']
    
@admin.register(Servicios)
class ServiciosAdmin(admin.ModelAdmin):
    list_display = ('id_servicio', 'nombre_servicio', 'precio_servicio', )
    search_fields = ['nombre_servicio']
    
@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('id_factura', 'nombre_producto', 'cantidad', 'total_sin_descuento', 'descuento', 'total_con_descuento', 'pago', 'usuario', 'servicios', )
    search_fields = ['id_factura','usuario']
    
@admin.register(Citas)
class CitasAdmin(admin.ModelAdmin):
    list_display = ('id_cita', 'hora_fecha', 'servicio', )
    search_fields = ['servicio']


