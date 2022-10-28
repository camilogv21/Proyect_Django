from pathlib import Path
from django.shortcuts import render,redirect
from .models import Usuario, Mascota, Producto, Factura, Servicios, Citas
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from .crypt import claveEncriptada
from os import remove, path
BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.
#=============================================================Perfil=======================================================================

def perfil(request):
    login = request.session.get('logueo', False)
    q =Usuario.objects.get(pk = login[0])
    contexto = {"perfil": q }
    return render(request,'Vitario/usuario/perfil.html',contexto)


def actualizarPerfil(request):

    if request.method == "POST":
        try:
            login = request.session.get('logueo', False)

            q = Usuario.objects.get(pk = login[0])

            q.nombre = request.POST["nombre"]
            q.direccion = request.POST["direccion"]
            q.telefono = request.POST["telefono"]
            q.correo = request.POST["correo"]

            if q.usuario != request.POST["usuario"]:
                try:
                    consulta = Usuario.objects.get(usuario = request.POST["usuario"])
                    raise Exception("El usuario ya existe")
                except Usuario.DoesNotExist:
                    q.usuario = request.POST["usuario"]
            else:
                q.usuario = request.POST["usuario"]

            if request.POST["clave"] != "":
                q.clave = claveEncriptada(request.POST["clave"])

            q.save()
            login[1] = q.nombre
            request.session["logueo"] = login

            messages.success(request,"Actualizacion correcta")
        except Usuario.DoesNotExist:
            messages.error(request,'No existe el usuario')
        except Exception as e:
            messages.error(request, f"Error: {e}")
    else:
        messages.warning(request, "No envio datos...")

    return redirect('Vitario:perfil')


"""         from django.core.mail import send_mail
            try:
                send_mail(
                    'Correo de Actualizacion',
                    'Hola como estas te escribo desde Vitario y tus datos han sido actualisados',
                    'galeanocamilo10@gmail.com',
                    ['jucagave10@outlook.como'],
                    fail_silently=False,
                )
                messages.info(request, "Correo enviado")
            except Exception as e:
                messages.error(request, f"Error: {e}") """

#==========================================================================================================================================

def inicio(request):
    
    return render(request, 'Vitario/index.html')

#====================================================LOGIN=================================================================================

def loginForm(request):
    return render(request,'Vitario/login/login.html')

def login(request):
        
    try:
        
        user = request.POST['usuario']
        pasw = claveEncriptada(request.POST["clave"])

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
            if request.FILES:
                # crear instacian de file sistem storage
                fss = FileSystemStorage()
                # capturar foto de formulario
                r = request.FILES["foto"]
                # cargar archivo alservidor
                file = fss.save("vitario/fotos/"+ r.name, r)
            else:
                file = "vitario/fotos/defaultUsu.png"
            
            q = Usuario(
                nombre = request.POST["nombre"],
                direccion = request.POST["direccion"],
                telefono = request.POST["telefono"],
                correo = request.POST["correo"],
                usuario = request.POST["usuario"],
                clave = claveEncriptada(request.POST["clave"]),
                rol = request.POST["rol"],
                foto = file
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
        # Primero eliminar la foto y despues el usuario
        ruta_foto = str(BASE_DIR) + str(a.foto.url)
        #averiguamos si la ruta es validad
        if path.exists(ruta_foto):
            #Borramos la ruta de la foto
            if a.foto.url != "/uploads/vitario/fotos/defaultUsu.png":
                remove(ruta_foto)
            # messages.success(request,"Foto eliminada correctamente")
        else:
            messages.error(request,"No se pudo eliminar la foto")
            raise Exception("Error!!! la foto no existe o no se encuentra")
        a.delete()
        messages.success(request,"Usuario eliminado correctamente")
        return redirect('vitario:usuario')
    except Usuario.DoesNotExist:
        messages.error(request,"Error!! el ueuario no existe")
    except Exception as e:
        messages.error(request,f'Error!! no se pudo eliminar el registro: {e}')

def usuarioRegistro(request):
    return render(request, 'Vitario/usuario/registro.html')
    
def editarUsuario(request, id):
    A = Usuario.objects.get(pk = id)
    contexto = { "datos" : A }
    return render(request, 'Vitario/usuario/editar_usuario.html', contexto)

def actualizarUsuario(request):
    try:
        if request.method == "POST":
            a = Usuario.objects.get(pk = request.POST["id"]) 
            if request.FILES:
                #Eliminar foto Anterior
                ruta_foto = str(BASE_DIR) + str(a.foto.url)
                if path.exists(ruta_foto):
                    if a.foto.url != "/uploads/vitario/fotos/defaultUsu.png":
                        remove(ruta_foto)
                else:
                    raise Exception("Error!!! la foto no existe o no se encuentra")
                #Guardar foto Nueva
                fss = FileSystemStorage()
                r = request.FILES["foto"]
                file = fss.save("vitario/fotos/"+ r.name, r)
                a.foto = file
            else:
                print ("El  usuario no cambio la foto")
                
            a.nombre = request.POST["nombre"]
            a.direccion = request.POST["direccion"]
            a.telefono = request.POST["telefono"]
            a.correo = request.POST["correo"]
            a.usuario = request.POST["usuario"]
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
            a.nombre_mascota = request.POST["nombre_mascota"]
            a.tipo_mascota = request.POST["tipo_mascota"]
            a.edad = request.POST["edad"]
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

# ===================================================PRODUCTO==============================================================================

def producto(request):
    
    q = Producto.objects.all()
    
    p = Paginator(q, 9)
    p_number = request.GET.get('page')
    
    q = p.get_page(p_number)
    
    contexto = {'page_obj': q}
    
    return render(request, 'Vitario/producto/listar_producto.html', contexto)

def productoConcentrado(request):
    
    q = Producto.objects.all()
    contexto = {'datos': q}
    return render(request, 'Vitario/producto/concentrado.html', contexto)

def productoMedi(request):
    
    q = Producto.objects.all()
    contexto = {'datos': q}
    return render(request, 'Vitario/producto/Medicamentos.html', contexto)

def productoAcce(request):
    
    q = Producto.objects.all()
    contexto = {'datos': q}
    return render(request, 'Vitario/producto/Accesorios.html', contexto)

def productoAlimen(request):
    
    q = Producto.objects.all()
    contexto = {'datos': q}
    return render(request, 'Vitario/producto/Alimentos.html', contexto)

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
            if request.FILES:
                fss = FileSystemStorage()
                r = request.FILES["foto"]
                file = fss.save("vitario/fotos/"+ r.name, r)
            else:
                file = "vitario/fotos/defaultPro.png"
            
            q = Producto(
                codigo_producto = request.POST["codigo_producto"],
                nombre_producto = request.POST["nombre_producto"],
                categoria = request.POST["categoria"],
                cantidad = request.POST["cantidad"],
                precio = request.POST["precio"],
                foto = file
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
        ruta_foto = str(BASE_DIR) + str(a.foto.url)
        if path.exists(ruta_foto):
            if a.foto.url != "/uploads/vitario/fotos/defaultPro.png":
                remove(ruta_foto)
        else:
            messages.error(request,"No se pudo eliminar la foto")
            raise Exception("Error!!! la foto no existe o no se encuentra")
        a.delete()
        messages.success(request,"Producto eliminado correctamente")
        return redirect('vitario:producto')
    except Producto.DoesNotExist:
        messages.error(request,"Error!! el ueuario no existe")
    except Exception as e:
        messages.error(request,f'Error!! no se pudo eliminar el registro: {e}')

def editarProducto(request, id):
    A = Producto.objects.get(pk = id)
    
    contexto = {"datos":A}
    return render(request, 'Vitario/producto/editar_producto.html', contexto)

def actualizarProducto(request):
    try:
        if request.method == "POST":
            a = Producto.objects.get(pk = request.POST["id"])
            if request.FILES:
                ruta_foto = str(BASE_DIR) + str(a.foto.url)
                if path.exists(ruta_foto):
                    if a.foto.url != "/uploads/vitario/fotos/defaultPro.png":
                        remove(ruta_foto)
                else:
                    raise Exception("Error!!! la foto no existe o no se encuentra")
                fss = FileSystemStorage()
                r = request.FILES["foto"]
                file = fss.save("vitario/fotos/"+ r.name, r)
                a.foto = file
            else:
                print ("No se cambio la foto")
                
            a.codigo_producto = request.POST["codigo_producto"]
            a.nombre_producto = request.POST["nombre_producto"]
            a.categoria = request.POST["categoria"]
            a.cantidad = request.POST["cantidad"]
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
    
    u = Usuario.objects.all()
    
    s = Servicios.objects.all()

    contexto = {'producto':p,'usuario':u,'servicio':s}

    return render(request, 'Vitario/factura/crear_factura.html', contexto)

def facturaGuardar(request):
    try:
        p = Producto.objects.get(pk = request.POST["nombre_producto"])
        u = Usuario.objects.get(pk = request.POST["usuario"])
        s = Servicios.objects.get(pk = request.POST["servicio"])
        
        if request.method == "POST":
            q = Factura(
                nombre_producto = p,
                cantidad = request.POST["cantidad"],
                total_sin_descuento = request.POST["total_sin_descuento"],
                descuento = request.POST["descuento"],
                total_con_descuento = request.POST["total_con_descuento"],
                medio_pago = request.POST["medio_pago"],
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

    p = Producto.objects.all()
    
    u = Usuario.objects.all()
    
    s = Servicios.objects.all()

    contexto = {'producto':p,'usuario':u,'servicio':s,"datos":A}

    return render(request, 'Vitario/factura/editar_factura.html', contexto)

def actualizarFactura(request):
    try:
        if request.method == "POST":
            a = Factura.objects.get(pk = request.POST["id"])
            a.cantidad = request.POST["cantidad"]
            a.total_sin_descuento = request.POST["total_sin_descuento"]
            a.descuento = request.POST["descuento"]
            a.total_con_descuento = request.POST["total_con_descuento"]
            a.medio_pago = request.POST["medio_pago"]
            # a.servicios = request.POST["servicio"]
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

def servicioTarjetas(request):
    
    q = Servicios.objects.all()
    contexto = {'datos': q}
    return render(request, 'Vitario/servicio/tarjeta_servicio.html', contexto)

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
            if request.FILES:
                fss = FileSystemStorage()
                r = request.FILES["foto"]
                file = fss.save("vitario/fotos/"+ r.name, r)
            else:
                file = "vitario/fotos/defaultMas.png"
                
            q = Servicios(
                codigo_servicio = request.POST["codigo_servicio"],
                nombre_servicio = request.POST["nombre_servicio"],
                precio_servicio = request.POST["precio_servicio"],
                foto = file
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
        ruta_foto = str(BASE_DIR) + str(a.foto.url)
        if path.exists(ruta_foto):
            if a.foto.url != "/uploads/vitario/fotos/defaultMas.png":
                remove(ruta_foto)
        else:
            messages.error(request,"No se pudo eliminar la foto")
            raise Exception("Error!!! la foto no existe o no se encuentra")
        a.delete()
        messages.success(request,"Servicio eliminado correctamente")
        return redirect('vitario:servicio')
    except Servicios.DoesNotExist:
        messages.error(request,"Error!! el ueuario no existe")
    except Exception as e:
        messages.error(request,f'Error!! no se pudo eliminar el registro: {e}')

    
def editarServicio(request, id):
    A = Servicios.objects.get(pk = id)
    contexto = {"datos":A}
    return render(request, 'Vitario/servicio/editar_servicio.html', contexto)

def actualizarServicio(request):
    try:
        if request.method == "POST":
            a = Servicios.objects.get(pk = request.POST["id"])
            if request.FILES:
                ruta_foto = str(BASE_DIR) + str(a.foto.url)
                if path.exists(ruta_foto):
                    if a.foto.url != "/uploads/vitario/fotos/defaultMas.png":
                        remove(ruta_foto)
                else:
                    raise Exception("Error!!! la foto no existe o no se encuentra")
                fss = FileSystemStorage()
                r = request.FILES["foto"]
                file = fss.save("vitario/fotos/"+ r.name, r)
                a.foto = file
            else:
                print ("No se cambio la foto")
                
            a.codigo_servicio = request.POST["codigo_servicio"]
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
    
    q = Usuario.objects.all()
    
    contexto = {'datos':p,"user":q}
    return render(request, 'Vitario/cita/crear_cita.html',contexto)

def citaGuardar(request):
    try:
        b = Servicios.objects.get(pk = request.POST["nombre_servicio"])
        
        q = Usuario.objects.get(pk = request.POST["nombre"])
        
        if request.method == "POST":
            q = Citas(
                usuario = q,
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
    
    b = Servicios.objects.all()
    
    q = Usuario.objects.all()
    contexto = {"datos":A,"user":q, "servi":b}
    return render(request, 'Vitario/cita/editar_cita.html', contexto)

def actualizarCita(request):
    try:
        if request.method == "POST":
            a = Citas.objects.get(pk = request.POST["id"])
            # a.usuario = request.POST["nombre"]
            a.hora_fecha = request.POST["hora_fecha"]
            # a.servicio = request.POST["servicio"]
            a.save()
            messages.success(request,"¡cita Actualizado correctamente!")
            return redirect('Vitario:cita')
        else:
            messages.warning(request,"¡No se han enviado datos!")
            return redirect('Vitario:cita')
    except Exception as e:
        messages.error(request,"Error" + str(e))
        return redirect('Vitario:cita')
    
def citaAgendar(request):
    p = Servicios.objects.all()
    
    q = Usuario.objects.all()
    
    contexto = {'datos':p,"user":q}
    return render(request, 'Vitario/cita/agendar_cita.html',contexto)

# =========================================================================================================================================