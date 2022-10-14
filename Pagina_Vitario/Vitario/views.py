from django.shortcuts import render,redirect
from .models import Usuario, Mascota, Pago, Producto, Factura, Servicios, Citas
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def inicio(request):
    
    return render(request, 'Vitario/index.html')

#====================================================LOGIN=================================================================================

def loginForm(request):
    return render(request,'Vitario/login/login.html')

def login(request):
        
    try:
        
        user = request.POST['usuario']
        pasw = request.POST['clave']

        q = Usuario.objects.get(usuario = user, clave = pasw)
        
        request.session["logueo"] = [q.id, q.nombre, q.rol, q.get_rol_display()]
        messages.success(request,"Bienvenido!!")
        return redirect('Vitario:inicio')
    except:
        messages.warning(request,"Hay que ingresar los datos")
        return redirect('Vitario:inicio')   

def loginC(request):
    try:
        del request.session["logueo"]
        messages.success(request, "Session cerrada")
    except Exception as e:
        messages.warning(request, "Ocurrio un error: ", e)
    return redirect('Vitario:inicio')

#==========================================================================================================================================

# ===================================================USUARIOS==============================================================================

def usuario(request):
    
    login = request.session.get('logueo',False)
    if login and (login[3] == "Administrador" or login[3] == "Empleado"):
        q = Usuario.objects.all()
        
        p = Paginator(q, 9)
        p_number = request.GET.get('page')
        
        q = p.get_page(p_number)
        
        contexto = {'page_obj': q}
        
        return render(request, 'Vitario/usuario/listar_usuario.html', contexto)

    else:
        if login and login[3] != "Administrador" and login[3] != "Empleado":
            messages.warning(request, "usted no esta autorizados para este modulo")
            return redirect('Vitario:inicio')
        else:    
            messages.warning(request, "No has iniciado session")
            return redirect('Vitario:loginForm')

def usuarioBuscar (request):
    
    if request.method == "POST":
        q = Usuario.objects.filter(
            Q(nombre__icontains = request.POST["buscar"])|
            Q(usuario__icontains = request.POST["buscar"])
            )
        p = Paginator(q, 9)
        p_number = request.GET.get('page')
        
        q = p.get_page(p_number)
        
        contexto = {'page_obj': q, 'Datos': request.POST["buscar"]}
        
        return render(request, 'Vitario/usuario/listar_usuario_ajax.html',contexto)
    else:
        messages.warning(request, "No se han enviado datos")
        return redirect('Vitario:usuario')
    
def usuarioFormulario(request):
    return render(request, 'Vitario/usuario/crear_usuario.html')

def usuarioGuardar(request):
    try:
        if request.method == "POST":
            q = Usuario(
                nombre = request.POST["nombre"],
                direccion = request.POST["direccion"],
                telefono = request.POST["telefono"],
                correo = request.POST["correo"],
                usuario = request.POST["usuario"],
                clave = request.POST["clave"],
                rol = request.POST["rol"],
            )
            q.save()
            messages.success(request,"¡Usuario guardado correctamente!")
            return redirect('Vitario:usuario')
        else:
            messages.warning(request, "¡No se han enviado datos!")
            return redirect('Vitario:usuario')
    except Exception as e:
        messages.error(request,"Error" + str(e))
        return redirect('Vitario:usuario')
    
def usuarioEliminar(request,id):
    try:
        a = Usuario.objects.get(pk = id)
        a.delete()
        return redirect('Vitario:usuario')
    except Usuario.DoesNotExist:
        return HttpResponse('ERROR: Usuario no encontrado')
    except Exception as e:
        return HttpResponse(f'ERROR: {e}')
    
def editarUsuario(request, id):
    A = Usuario.objects.get(pk = id)
    contexto = { "datos" : A }
    return render(request, 'Vitario/usuario/editar_usuario.html', contexto)

def actualizarUsuario(request):
    try:
        if request.method == "POST":
            a = Usuario.objects.get(pk = request.POST["id"])
            a.nombre = request.POST["nombre"]
            a.direccion = request.POST["direccion"]
            a.telefono = request.POST["telefono"]
            a.correo = request.POST["correo"]
            a.usuario = request.POST["usuario"]
            a.clave = request.POST["clave"]
            a.rol = request.POST["rol"]
            a.save()
            messages.success(request,"¡Usuario Actualizado correctamente!")
            return redirect('Vitario:usuario')
        else:
            messages.warning(request,"¡No se han enviado datos!")
            return redirect('Vitario:usuario')
    except Exception as e:
        messages.error(request,"Error" + str(e))
        return redirect('Vitario:usuario')
    
# ========================================================================================================================================

# ===================================================MASCOTAS==============================================================================

def mascota(request):
    
    q = Mascota.objects.all()
    
    p = Paginator(q, 9)
    p_number = request.GET.get('page')
    
    q = p.get_page(p_number)
    
    contexto = {'page_obj': q}
    
    return render(request, 'Vitario/mascota/listar_mascota.html', contexto)

def mascotaBuscar (request):
    
    if request.method == "POST":
        q = Mascota.objects.filter(
            Q(nombre_mascota__icontains = request.POST["buscar"])|
            Q(tipo_mascota__icontains = request.POST["buscar"])
            )
        p = Paginator(q, 9)
        p_number = request.GET.get('page')
        
        q = p.get_page(p_number)
        
        contexto = {'page_obj': q, 'Datos': request.POST["buscar"]}
        
        return render(request, 'Vitario/mascota/listar_mascota_ajax.html', contexto)
    else:
        messages.warning(request, "No se han enviado datos")
        return redirect('Vitario:mascota')
    
def mascotaFormulario(request):
    q = Usuario.objects.all()
    contexto = {'datos':q}
    return render(request, 'Vitario/mascota/crear_mascota.html',contexto)

def mascotaGuardar(request):
    try:
        a = Usuario.objects.get(pk = request.POST["usuario"])
        if request.method == "POST":
            q = Mascota(
                id_mascota = request.POST["id_mascota"],
                nombre_mascota = request.POST["nombre_mascota"],
                tipo_mascota = request.POST["tipo_mascota"],
                edad = request.POST["edad"],
                usuario = a,
            )
            q.save()
            messages.success(request,"¡mascota guardado correctamente!")
            return redirect('Vitario:mascota')
        else:
            messages.warning(request, "¡No se han enviado datos!")
            return redirect('Vitario:mascota')
    except Exception as e:
        messages.error(request,"Error" + str(e))
        return redirect('Vitario:mascota')
    
def mascotaEliminar(request,id):
    try:
        a = Mascota.objects.get(pk = id)
        a.delete()
        return redirect('Vitario:mascota')
    except Mascota.DoesNotExist:
        return HttpResponse('ERROR: mascota no encontrado')
    except Exception as e:
        return HttpResponse(f'ERROR: {e}')
    
def editarMascota(request, id):
    A = Mascota.objects.get(pk = id)
    contexto = {"datos":A}
    return render(request, 'Vitario/mascota/editar_mascota.html', contexto)

def actualizarMascota(request):
    try:
        if request.method == "POST":
            a = Mascota.objects.get(pk = request.POST["id"])
            a.id_mascota = request.POST["id_mascota"]
            a.nombre_mascota = request.POST["nombre_mascota"]
            a.tipo_mascota = request.POST["tipo_mascota"]
            a.edad = request.POST["edad"]
            a.usuario = request.POST["usuario"]
            a.save()
            messages.success(request,"¡mascota Actualizado correctamente!")
            return redirect('Vitario:mascota')
        else:
            messages.warning(request,"¡No se han enviado datos!")
            return redirect('Vitario:mascota')
    except Exception as e:
        messages.error(request,"Error" + str(e))
        return redirect('Vitario:mascota')

# =========================================================================================================================================

# ===================================================PAGO==================================================================================

def pago(request):
    
    q = Pago.objects.all()
    
    p = Paginator(q, 9)
    p_number = request.GET.get('page')
    
    q = p.get_page(p_number)
    
    contexto = {'page_obj': q}
    
    return render(request, 'Vitario/pago/listar_pago.html', contexto)

def pagoBuscar (request):
    
    if request.method == "POST":
        q = Pago.objects.filter(
            Q(medio_pago__icontains = request.POST["buscar"])
            )
        p = Paginator(q, 9)
        p_number = request.GET.get('page')
        
        q = p.get_page(p_number)
        
        contexto = {'page_obj': q, 'Datos': request.POST["buscar"]}
        
        return render(request, 'Vitario/pago/listar_pago_ajax.html',contexto)
    else:
        messages.warning(request, "No se han enviado datos")
        return redirect('Vitario:pago')
    
def pagoFormulario(request):
    return render(request, 'Vitario/pago/crear_pago.html')

def pagoGuardar(request):
    try:
        if request.method == "POST":
            q = Pago(
                id_pago = request.POST["id_pago"],
                medio_pago = request.POST["medio_pago"],
            )
            q.save()
            messages.success(request,"¡pago guardado correctamente!")
            return redirect('Vitario:pago')
        else:
            messages.warning(request, "¡No se han enviado datos!")
            return redirect('Vitario:pago')
    except Exception as e:
        messages.error(request,"Error" + str(e))
        return redirect('Vitario:pago')
    
def pagoEliminar(request,id):
    try:
        a = Pago.objects.get(pk = id)
        a.delete()
        return redirect('Vitario:pago')
    except Pago.DoesNotExist:
        return HttpResponse('ERROR: pago no encontrado')
    except Exception as e:
        return HttpResponse(f'ERROR: {e}')
    
def editarPago(request, id):
    A = Pago.objects.get(pk = id)
    contexto = {"datos":A}
    return render(request, 'Vitario/pago/editar_pago.html', contexto)

def actualizarPago(request):
    try:
        if request.method == "POST":
            a = Pago.objects.get(pk = request.POST["id"])
            a.id_pago = request.POST["id_pago"]
            a.medio_pago = request.POST["medio_pago"]
            a.save()
            messages.success(request,"¡pago Actualizado correctamente!")
            return redirect('Vitario:pago')
        else:
            messages.warning(request,"¡No se han enviado datos!")
            return redirect('Vitario:pago')
    except Exception as e:
        messages.error(request,"Error" + str(e))
        return redirect('Vitario:pago')
    

# =========================================================================================================================================

# ===================================================PRODUCTO==============================================================================

def producto(request):
    
    q = Producto.objects.all()
    
    p = Paginator(q, 9)
    p_number = request.GET.get('page')
    
    q = p.get_page(p_number)
    
    contexto = {'page_obj': q}
    
    return render(request, 'Vitario/producto/listar_producto.html', contexto)

def productoBuscar (request):
    
    if request.method == "POST":
        q = Producto.objects.filter(
            Q(nombre_producto__icontains = request.POST["buscar"])|
            Q(tipo_producto__icontains = request.POST["buscar"])
            )
        p = Paginator(q, 9)
        p_number = request.GET.get('page')
        
        q = p.get_page(p_number)
        
        contexto = {'page_obj': q, 'Datos': request.POST["buscar"]}
        
        return render(request, 'Vitario/producto/listar_producto_ajax.html',contexto)
    else:
        messages.warning(request, "No se han enviado datos")
        return redirect('Vitario:producto')
    
def productoFormulario(request):
    return render(request, 'Vitario/producto/crear_producto.html')

def productoGuardar(request):
    try:
        if request.method == "POST":
            q = Producto(
                codigo_producto = request.POST["codigo_producto"],
                nombre_producto = request.POST["nombre_producto"],
                cantidad = request.POST["cantidad"],
                tipo_producto = request.POST["tipo_producto"],
                precio = request.POST["precio"],
            )
            q.save()
            messages.success(request,"¡producto guardado correctamente!")
            return redirect('Vitario:producto')
        else:
            messages.warning(request, "¡No se han enviado datos!")
            return redirect('Vitario:producto')
    except Exception as e:
        messages.error(request,"Error" + str(e))
        return redirect('Vitario:producto')
    
def productoEliminar(request,id):
    try:
        a = Producto.objects.get(pk = id)
        a.delete()
        return redirect('Vitario:producto')
    except Producto.DoesNotExist:
        return HttpResponse('ERROR: producto no encontrado')
    except Exception as e:
        return HttpResponse(f'ERROR: {e}')
    
def editarProducto(request, id):
    A = Producto.objects.get(pk = id)
    contexto = {"datos":A}
    return render(request, 'Vitario/producto/editar_producto.html', contexto)

def actualizarProducto(request):
    try:
        if request.method == "POST":
            a = Producto.objects.get(pk = request.POST["id"])
            a.codigo_producto = request.POST["codigo_producto"]
            a.nombre_product = request.POST["nombre_product"]
            a.cantidad = request.POST["cantidad"]
            a.tipo_producto = request.POST["tipo_producto"]
            a.precio = request.POST["precio"]
            a.save()
            messages.success(request,"¡producto Actualizado correctamente!")
            return redirect('Vitario:producto')
        else:
            messages.warning(request,"¡No se han enviado datos!")
            return redirect('Vitario:producto')
    except Exception as e:
        messages.error(request,"Error" + str(e))
        return redirect('Vitario:producto')

# =========================================================================================================================================

# ===================================================FACTURA===============================================================================

def factura(request):
    
    q = Factura.objects.all()
    
    p = Paginator(q, 9)
    p_number = request.GET.get('page')
    
    q = p.get_page(p_number)
    
    contexto = {'page_obj': q}
    
    return render(request, 'Vitario/factura/listar_factura.html', contexto)

def facturaBuscar (request):
    
    if request.method == "POST":
        q = Factura.objects.filter(
            Q(id_factura__icontains = request.POST["buscar"])
            )
        p = Paginator(q, 9)
        p_number = request.GET.get('page')
        
        q = p.get_page(p_number)
        
        contexto = {'page_obj': q, 'Datos': request.POST["buscar"]}
        
        return render(request, 'Vitario/factura/listar_factura_ajax.html',contexto)
    else:
        messages.warning(request, "No se han enviado datos")
        return redirect('Vitario:factura')
    
def facturaFormulario(request):
    p = Producto.objects.all()
    contextop = {'datop':p}
    
    q = Pago.objects.all()
    contexto = {'datoq':q}
    
    u = Usuario.objects.all()
    contextou = {'datou':u}
    
    s = Servicios.objects.all()
    contextos = {'datos':s}
    
    
    
    return render(request, 'Vitario/factura/crear_factura.html',{"contexto" : contexto , 
                                                                "contextop": contextop , 
                                                                "contextos": contextos , 
                                                                "contextou" : contextou })

def facturaGuardar(request):
    try:
        p = Producto.objects.get(pk = request.POST["nombre_producto"])
        b = Pago.objects.get(pk = request.POST["pago"])
        u = Usuario.objects.get(pk = request.POST["usuario"])
        s = Servicios.objects.get(pk = request.POST["servicios"])
        
        if request.method == "POST":
            q = Factura(
                id_factura = request.POST["id_factura"],
                direccion = request.POST["direccion"],
                nombre_producto = p,
                cantidad = request.POST["cantidad"],
                total_sin_descuento = request.POST["total_sin_descuento"],
                descuento = request.POST["descuento"],
                total_con_descuento = request.POST["total_con_descuento"],
                pago = b,
                usuario = u,
                servicios = s,
            )
            q.save()
            messages.success(request,"¡factura guardado correctamente!")
            return redirect('Vitario:factura')
        else:
            messages.warning(request, "¡No se han enviado datos!")
            return redirect('Vitario:factura')
    except Exception as e:
        messages.error(request,"Error" + str(e))
        return redirect('Vitario:factura')
    
def facturaEliminar(request,id):
    try:
        a = Factura.objects.get(pk = id)
        a.delete()
        return redirect('Vitario:factura')
    except Factura.DoesNotExist:
        return HttpResponse('ERROR: factura no encontrado')
    except Exception as e:
        return HttpResponse(f'ERROR: {e}')
    
def editarFactura(request, id):
    A = Factura.objects.get(pk = id)
    contexto = {"datos":A}
    return render(request, 'Vitario/factura/editar_factura.html', contexto)

def actualizarFactura(request):
    try:
        if request.method == "POST":
            a = Factura.objects.get(pk = request.POST["id"])
            a.id_factura = request.POST["id_factura"]
            a.cantidad = request.POST["cantidad"]
            a.total_sin_descuento = request.POST["total_sin_descuento"]
            a.descuento = request.POST["descuento"]
            a.total_con_descuento = request.POST["total_con_descuento"]
            a.pago = request.POST["pago"]
            a.usuario = request.POST["usuario"]
            a.servicios = request.POST["servicios"]
            a.save()
            messages.success(request,"¡factura Actualizado correctamente!")
            return redirect('Vitario:factura')
        else:
            messages.warning(request,"¡No se han enviado datos!")
            return redirect('Vitario:factura')
    except Exception as e:
        messages.error(request,"Error" + str(e))
        return redirect('Vitario:factura')

# =========================================================================================================================================

# ===================================================SERVICIO==============================================================================

def servicio(request):
    
    q = Servicios.objects.all()
    
    p = Paginator(q, 9)
    p_number = request.GET.get('page')
    
    q = p.get_page(p_number)
    
    contexto = {'page_obj': q}
    
    return render(request, 'Vitario/servicio/listar_servicio.html', contexto)

def servicioBuscar (request):
    
    if request.method == "POST":
        q = Servicios.objects.filter(
            Q(nombre__icontains = request.POST["buscar"])|
            Q(servicio__icontains = request.POST["buscar"])
            )
        p = Paginator(q, 9)
        p_number = request.GET.get('page')
        
        q = p.get_page(p_number)
        
        contexto = {'page_obj': q, 'Datos': request.POST["buscar"]}
        
        return render(request, 'Vitario/servicio/listar_servicio_ajax.html',contexto)
    else:
        messages.warning(request, "No se han enviado datos")
        return redirect('Vitario:servicio')
    
def servicioFormulario(request):
    return render(request, 'Vitario/servicio/crear_servicio.html')

def servicioGuardar(request):
    try:
        if request.method == "POST":
            q = Servicios(
                id_servicio = request.POST["id_servicio"],
                nombre_servicio = request.POST["nombre_servicio"],
                precio_servicio = request.POST["precio_servicio"],
            )
            q.save()
            messages.success(request,"¡servicio guardado correctamente!")
            return redirect('Vitario:servicio')
        else:
            messages.warning(request, "¡No se han enviado datos!")
            return redirect('Vitario:servicio')
    except Exception as e:
        messages.error(request,"Error" + str(e))
        return redirect('Vitario:servicio')
    
def servicioEliminar(request,id):
    try:
        a = Servicios.objects.get(pk = id)
        a.delete()
        return redirect('Vitario:servicio')
    except Servicios.DoesNotExist:
        return HttpResponse('ERROR: servicio no encontrado')
    except Exception as e:
        return HttpResponse(f'ERROR: {e}')
    
def editarServicio(request, id):
    A = Servicios.objects.get(pk = id)
    contexto = {"datos":A}
    return render(request, 'Vitario/servicio/editar_servicio.html', contexto)

def actualizarServicio(request):
    try:
        if request.method == "POST":
            a = Servicios.objects.get(pk = request.POST["id"])
            a.id_servicio = request.POST["id_servicio"]
            a.nombre_servicio = request.POST["nombre_servicio"]
            a.precio_servicio = request.POST["precio_servicio"]
            a.save()
            messages.success(request,"¡servicio Actualizado correctamente!")
            return redirect('Vitario:servicio')
        else:
            messages.warning(request,"¡No se han enviado datos!")
            return redirect('Vitario:servicio')
    except Exception as e:
        messages.error(request,"Error" + str(e))
        return redirect('Vitario:servicio')

# =========================================================================================================================================

# ===================================================CITAS=================================================================================

def cita(request):
    
    q = Citas.objects.all()
    
    p = Paginator(q, 9)
    p_number = request.GET.get('page')
    
    q = p.get_page(p_number)
    
    contexto = {'page_obj': q}
    
    return render(request, 'Vitario/cita/listar_cita.html', contexto)

def citaBuscar (request):
    
    if request.method == "POST":
        q = Citas.objects.filter(
            Q(nombre__icontains = request.POST["buscar"])|
            Q(cita__icontains = request.POST["buscar"])
            )
        p = Paginator(q, 9)
        p_number = request.GET.get('page')
        
        q = p.get_page(p_number)
        
        contexto = {'page_obj': q, 'Datos': request.POST["buscar"]}
        
        return render(request, 'Vitario/cita/listar_cita_ajax.html',contexto)
    else:
        messages.warning(request, "No se han enviado datos")
        return redirect('Vitario:cita')
    
def citaFormulario(request):
    p = Servicios.objects.all()
    contexto = {'datos':p}
    return render(request, 'Vitario/cita/crear_cita.html',contexto)

def citaGuardar(request):
    try:
        b = Servicios.objects.get(pk = request.POST["nombre_servicio"])
        if request.method == "POST":
            q = Citas(
                id_cita = request.POST["id_cita"],
                hora_fecha = request.POST["hora_fecha"],
                servicio = b,
            )
            q.save()
            messages.success(request,"¡cita guardado correctamente!")
            return redirect('Vitario:cita')
        else:
            messages.warning(request, "¡No se han enviado datos!")
            return redirect('Vitario:cita')
    except Exception as e:
        messages.error(request,"Error" + str(e))
        return redirect('Vitario:cita')
    
def citaEliminar(request,id):
    try:
        a = Citas.objects.get(pk = id)
        a.delete()
        return redirect('Vitario:cita')
    except Citas.DoesNotExist:
        return HttpResponse('ERROR: cita no encontrado')
    except Exception as e:
        return HttpResponse(f'ERROR: {e}')
    
def editarCita(request, id):
    A = Citas.objects.get(pk = id)
    contexto = {"datos":A}
    return render(request, 'Vitario/cita/editar_cita.html', contexto)

def actualizarCita(request):
    try:
        if request.method == "POST":
            a = Citas.objects.get(pk = request.POST["id"])
            a.id_cita = request.POST["id_cita"]
            a.hora_fecha = request.POST["hora_fecha"]
            a.servicio = request.POST["servicio"]
            a.save()
            messages.success(request,"¡cita Actualizado correctamente!")
            return redirect('Vitario:cita')
        else:
            messages.warning(request,"¡No se han enviado datos!")
            return redirect('Vitario:cita')
    except Exception as e:
        messages.error(request,"Error" + str(e))
        return redirect('Vitario:cita')

# =========================================================================================================================================

