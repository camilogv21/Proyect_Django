from django.contrib import admin
from .models import Usuario, Mascota, Producto, Factura, Servicios, Citas, Disponibilidad
# Register your models here.

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ( 'nombre', 'direccion', 'telefono', 'correo', 'usuario', 'clave', 'rol', 'foto', 'verfoto')
    search_fields = [ 'nombre','rol']
    
    def verfoto(self, obj):
        from django.utils.html import format_html
        foto = obj.foto.url
        
        return format_html(f"<a href='{foto}' target='_blank'> <img src='{foto}' width='10%' /> </a>")
    
@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ( 'nombre_mascota', 'tipo_mascota', 'edad', 'usuario', )
    search_fields = ['nombre_mascota', 'usuario']
    
    def edad(self, obj):
        from datetime import date
        hoy = date.today()
        
        edad = hoy.year - obj.fecha_nacimiento.year - ((hoy.month,hoy.day)<(obj.fecha_nacimiento.month, obj.fecha_nacimiento.day))
        return edad
    
    
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo_producto', 'nombre_producto', 'categoria', 'cantidad',  'precio', 'foto', 'verfoto' )
    search_fields = ['id_producto', 'nombre_producto']
    
    def verfoto(self, obj):
        from django.utils.html import format_html
        foto = obj.foto.url
        
        return format_html(f"<a href='{foto}' target='_blank'> <img src='{foto}' width='10%' /> </a>")
    
@admin.register(Servicios)
class ServiciosAdmin(admin.ModelAdmin):
    list_display = ('codigo_servicio', 'nombre_servicio', 'precio_servicio','foto','verfoto' )
    search_fields = ['nombre_servicio']
    
    def verfoto(self, obj):
        from django.utils.html import format_html
        foto = obj.foto.url
        
        return format_html(f"<a href='{foto}' target='_blank'> <img src='{foto}' width='10%' /> </a>")
    
@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ( 'nombre_producto', 'cantidad', 'total_sin_descuento', 'descuento', 'total_con_descuento', 'medio_pago', 'usuario', 'servicios', )
    search_fields = ['id_factura','usuario']

@admin.register(Disponibilidad)
class disponibilidadAdmin(admin.ModelAdmin):
    list_display = ('empleado','dia', 'hora', 'fecha_inicio', 'fecha_fin', 'reservado',)
    search_fields = ['servicio']

@admin.register(Citas)
class CitasAdmin(admin.ModelAdmin):
    list_display = ( 'usuario', 'disponibilidad', 'estado' , )
    search_fields = ['usuario']


