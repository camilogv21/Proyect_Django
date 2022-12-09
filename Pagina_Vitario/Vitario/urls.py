from django.urls import path

from . import views

app_name = "Vitario"

urlpatterns = [
    path('', views.inicio, name="inicio"),

    path('loginForm/',views.loginForm, name="loginForm"),
    path('login/',views.login, name="login"),
    path('loginC/',views.loginC, name="login_cerrar"),
    
    path('usuario/', views.usuario, name="usuario"),
    path('crear_usuario/', views.usuarioFormulario, name="crear_usuario"),
    path('guardar_usuario/', views.usuarioGuardar, name="guardar_usuario"),
    path('eliminar_usuario/<int:id>',views.usuarioEliminar, name="eliminar_usuario"),
    path('editarusUario/<int:id>',views.editarUsuario, name="editar_usuario"),
    path('actualizarUsuario/',views.actualizarUsuario, name="actualizar_usuario"),
    path('BuscarUsuario/',views.usuarioBuscar, name="Buscar_usuario"),
    path('registro/',views.usuarioRegistro, name="Registro"),
    
    path('mascota/', views.mascota, name="mascota"),
    path('crear_mascota/', views.mascotaFormulario, name="crear_mascota"),
    path('guardar_mascota/', views.mascotaGuardar, name="guardar_mascota"),
    path('eliminar_mascota/<int:id>',views.mascotaEliminar, name="eliminar_mascota"),
    path('editarMascota/<int:id>',views.editarMascota, name="editar_mascota"),
    path('actualizarMascota/',views.actualizarMascota, name="actualizar_mascota"),
    path('BuscarMascota/',views.mascotaBuscar, name="Buscar_mascota"),
    
    path('producto/', views.producto, name="producto"),
    path('crear_producto/', views.productoFormulario, name="crear_producto"),
    path('guardar_producto/', views.productoGuardar, name="guardar_producto"),
    path('eliminar_producto/<int:id>',views.productoEliminar, name="eliminar_producto"),
    path('editarProducto/<int:id>',views.editarProducto, name="editar_producto"),
    path('actualizarProducto/',views.actualizarProducto, name="actualizar_producto"),
    path('BuscarProducto/',views.productoBuscar, name="Buscar_producto"),
    path('concentrado/', views.productoConcentrado, name="concentrado"),
    path('accesorio/', views.productoAccesorio, name="accesorio"),
    path('medicamento/', views.productoMedicamento, name="medicamento"),
    path('premio/', views.productoPremios, name="premio"),
    
    path('factura/', views.factura, name="factura"),
    path('crear_factura/', views.facturaFormulario, name="crear_factura"),
    path('guardar_factura/', views.facturaGuardar, name="guardar_factura"),
    path('eliminar_factura/<int:id>',views.facturaEliminar, name="eliminar_factura"),
    path('editarFactura/<int:id>',views.editarFactura, name="editar_factura"),
    path('actualizarFactura/',views.actualizarFactura, name="actualizar_factura"),
    path('BuscarFactura/',views.facturaBuscar, name="Buscar_factura"),
    
    path('servicio/', views.servicio, name="servicio"),
    path('crear_servicio/', views.servicioFormulario, name="crear_servicio"),
    path('guardar_servicio/', views.servicioGuardar, name="guardar_servicio"),
    path('eliminar_servicio/<int:id>',views.servicioEliminar, name="eliminar_servicio"),
    path('editarServicio/<int:id>',views.editarServicio, name="editar_servicio"),
    path('actualizarServicio/',views.actualizarServicio, name="actualizar_servicio"),
    path('BuscarServicio/',views.servicioBuscar, name="Buscar_servicio"),
    path('tarjeta_servicio/', views.servicioTarjetas, name="tarjetaservicio"),
    
    path('cita/', views.cita, name="cita"),
    path('crear_cita/', views.citaFormulario, name="crear_cita"),
    path('guardar_cita/', views.citaGuardar, name="guardar_cita"),
    path('eliminar_cita/<int:id>',views.citaEliminar, name="eliminar_cita"),
    path('editarCita/<int:id>',views.editarCita, name="editar_cita"),
    path('actualizarCita/',views.actualizarCita, name="actualizar_cita"),
    path('BuscarCita/',views.citaBuscar, name="Buscar_cita"),
    path('agendar/', views.Agendar, name="agendar"),
    path('veragenda/<str:fecha>/', views.verAgenda, name="veragenda"),
    path('guardaragenda/<str:fecha>/', views.guardarAgenda, name="guardaragenda"),
    path('apartarCita/', views.apartarCita, name="apartarCita"),
    path('formularioApartarCita/<int:empleado>', views.formularioApartarCitas, name="formularioApartarCita"),
    
    path('perfil/',views.perfil, name="perfil"),
    path('actualizarPerfil/',views.actualizarPerfil, name="actualizar_perfil"),
    
    path('carrito/',views.carritoCompra, name="carrito"),
    path('agregar/<int:producto_id>/',views.agregar_producto, name="agregar"),
    path('restar/<int:producto_id>/',views.restar_producto, name="restar"),
    path('limpiar/',views.limpiar_carrito, name="limpiar"),
]