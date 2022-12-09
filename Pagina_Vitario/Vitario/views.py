from pathlib import Path
from django.shortcuts import render,redirect

from Vitario.Carrito import Carrito
from .models import Usuario, Mascota, Producto, Factura, Servicios, Citas, Disponibilidad
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from .crypt_1 import claveEncriptada
from os import remove, path
BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.
#===================================================Perfil==============================================================

"""Obtiene la identificación del usuario de la sesión, luego obtiene los datos del usuario de la base
de datos y luego los pasa a la plantilla
    :param request: El objeto de la solicitud
    :return: El perfil del usuario.
"""
def perfil(request):

    login = request.session.get('logueo', False)
    q =Usuario.objects.get(pk = login[0])
    contexto = {"perfil": q }
    return render(request,'Vitario/usuario/perfil.html',contexto)

"""Actualiza el perfil del usuario.
    :param request: El objeto de la solicitud
    :return: una redirección a la vista de perfil.
"""

def actualizarPerfil(request):

    if request.method == "POST":
        try:
            # Obtener los datos del usuario de la base de datos y actualizarlos.
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

#=======================================================================================================================

"""Toma una solicitud y devuelve una respuesta.
    :param request: El objeto de solicitud es un objeto HttpRequest.
    :return: La función de renderizado está siendo devuelta.
"""

def inicio(request):
    return render(request, 'Vitario/index.html')

#====================================================LOGIN==============================================================

def loginForm(request):
    return render(request,'Vitario/login/login.html')

"""En esta funcion nos permite saber i el usuario existe y si existe que inicie sesión y rediríjalo a la página de 
inicio. y si no existe rediríjalos a la página de inicio de sesión.   
    :param request: El objeto de la solicitud
    :return: El usuario está siendo devuelto.
"""

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

"""Esta funcion elimina la variable de sesión "Cierra la sesión" y redirige a la página de inicio
    :param request: El objeto de la solicitud
    :return: la función de redirección.
"""

def loginC(request):

    try:
        del request.session["logueo"]
        messages.success(request, "Session cerrada")
    except Exception as e:
        messages.warning(request, "Ocurrio un error: ", e)
    return redirect('Vitario:inicio')

#=======================================================================================================================

# ===============================================USUARIOS===============================================================

"""Esta funcion consulta si el usuario ha iniciado sesión y es administrador o empleado y que muestre la lista 
de usuarios. Si el usuario no ha iniciado sesión o no es administrador o empleado, se le redirige a la página de inicio 
de sesión.
    :param request: El objeto de la solicitud
    :return:un objeto de renderizado.
"""

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

"""Si la solicitud es una solicitud POST, filtre el modelo Usuario por el término de búsqueda, pagine
    los resultados y represente los resultados en una plantilla
    
    :param request: El objeto de la solicitud
    :return: una representación de la plantilla 'Vitary/users/list_users_ajax.html'
"""
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
    
"""Representa la plantilla y la devuelve
    :param request: El objeto de la solicitud
    :return: La función de renderizado está siendo devuelta.
"""
def usuarioFormulario(request):
    return render(request, 'Vitario/usuario/crear_usuario.html')

"""Si el método de solicitud es POST, guarde el archivo en el servidor; de lo contrario, establezca el
    archivo en la imagen predeterminada
    :param request: El objeto de la solicitud
    :return: una redirección a la url Vitario:usuario.
"""
def usuarioGuardar(request):
    try:
        if request.method == "POST":
                # Guardando la imagen en el servidor.
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
    
"""Elimina un usuario de la base de datos y elimina la foto del usuario del servidor
    :param request: El objeto de la solicitud
    :param id: El id del objeto que se va a eliminar
    :return: una redirección a la url vitarium:usuario.
"""
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
    
"""Obtiene al usuario con la identificación que se pasa como parámetro y luego devuelve los datos del usuario.
    :param request: El objeto de solicitud utilizado para generar esta respuesta
    :param id: El id del objeto que desea editar
    :return: El objeto A está siendo devuelto.
"""
def editarUsuario(request, id):
    A = Usuario.objects.get(pk = id)
    contexto = { "datos" : A }
    return render(request, 'Vitario/usuario/editar_usuario.html', contexto)

"""Si el método de solicitud es POST, obtenga el usuario con la identificación de la solicitud, si la
    solicitud tiene un archivo, elimine la foto anterior, guarde la nueva foto, guarde al usuario con
    los nuevos datos
    :param request: El objeto de la solicitud
    :return: una redirección a la url 'Vitary:usuario'
"""
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

"""Toma una solicitud, obtiene todos los objetos del modelo Mascota,  obtiene el número de
    página de la solicitud, obtiene la página del paginador y luego devuelve una representación de la
    página.
    :param request: El objeto de la solicitud
    :return: un objeto de renderizado.
"""
def mascota(request):
    
    q = Mascota.objects.all()
    
    p = Paginator(q, 9)
    p_number = request.GET.get('page')
    
    q = p.get_page(p_number)
    
    contexto = {'page_obj': q}
    
    return render(request, 'Vitario/mascota/listar_mascota.html', contexto)

"""Si la solicitud es una solicitud POST, filtre los objetos Mascota por el término de búsqueda, pagine
    los resultados y represente los resultados en una plantilla.
    
    :param request: El objeto de la solicitud
    :return: representación de la plantilla 'Vitario/pet/list_pet_ajax.html'
"""
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
    
"""Toma una solicitud, obtiene todos los usuarios de la base de datos y luego presenta la plantilla con
        los usuarios como contexto
        
        :param request: El objeto de solicitud es un objeto de Python que contiene metadatos sobre la
        solicitud enviada al servidor
        :return: La función mascotaFormulario está devolviendo la función render.
"""
def mascotaFormulario(request):
    q = Usuario.objects.all()
    contexto = {'datos':q}
    return render(request, 'Vitario/mascota/crear_mascota.html',contexto)

"""Si el método de solicitud es POST, cree un nuevo objeto Mascota con los datos de la solicitud y
    guárdelo en la base de datos.
    
    :param request: El objeto de la solicitud
    :return: El mensaje de error está siendo devuelto.
"""
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
    
"""Elimina una mascota de la base de datos.
    :param request: El objeto de solicitud es un objeto Django que contiene metadatos sobre la solicitud
    enviada al servidor
    :param id: El id del objeto que se va a eliminar
    :return: la respuesta de la solicitud.
"""
def mascotaEliminar(request,id):
    try:
        a = Mascota.objects.get(pk = id)
        a.delete()
        return redirect('Vitario:mascota')
    except Mascota.DoesNotExist:
        return HttpResponse('ERROR: mascota no encontrado')
    except Exception as e:
        return HttpResponse(f'ERROR: {e}')

"""Obtiene los datos de la base de datos y los envía a la plantilla.
    
    :param request: El objeto de la solicitud
    :param id: El id del objeto que desea editar
    :return: la plantilla 'Vitario/pet/edit_pet.html'
"""
def editarMascota(request, id):
    A = Mascota.objects.get(pk = id)
    contexto = {"datos":A}
    return render(request, 'Vitario/mascota/editar_mascota.html', contexto)

"""Intenta actualizar una mascota, si falla, redirige a la página de mascotas y muestra un mensaje de
    error
    :param request: El objeto de la solicitud
    :return: la función de redirección.
"""
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

"""Obtiene todos los productos, los pagina y luego representa la página
    
    :param request: El objeto de la solicitud
    :return: Una lista de objetos.
"""
def producto(request):
    
    q = Producto.objects.all()
    
    p = Paginator(q, 9)
    p_number = request.GET.get('page')
    
    q = p.get_page(p_number)
    
    contexto = {'page_obj': q}
    
    return render(request, 'Vitario/producto/listar_producto.html', contexto)

"""Si la solicitud es una solicitud POST, filtre los objetos Producto por el término de búsqueda,
    pagine los resultados y presente los resultados en la plantilla listar_producto_ajax.html
    
    :param request: El objeto de la solicitud
    :return: a render of the template 'Vitario/producto/listar_producto_ajax.html'
"""
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

"""Toma una solicitud, verifica si es una solicitud POST, verifica si tiene un archivo, guarda el
    archivo, guarda el nombre del archivo en la base de datos y redirige a la página del producto
    
    :param request: El objeto de la solicitud
    :return: La ruta del archivo.
"""
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
    
"""Elimina un producto de la base de datos y elimina la imagen del servidor
    
    :param request: El objeto de la solicitud
    :param id: El id del objeto que se va a eliminar
    :return: la función de redirección.
"""
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

"""Obtiene el producto con la identificación que se pasó en la URL y luego lo pasa a la plantilla
    
    :param request: El objeto de la solicitud
    :param id: El id del objeto que desea editar
    :return: la función de renderizado.
"""
def editarProducto(request, id):
    A = Producto.objects.get(pk = id)
    
    contexto = {"datos":A}
    return render(request, 'Vitario/producto/editar_producto.html', contexto)

"""Si el método de solicitud es POST, obtenga el producto con la identificación de la solicitud, si la
    solicitud tiene un archivo, obtenga la ruta del archivo, si el archivo existe, elimínelo, guarde el
    nuevo archivo, guarde el producto con los nuevos datos, y redirigir a la página del producto
    
    :param request: El objeto de la solicitud
    :return: una redirección a la página del producto.
"""
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

def productoConcentrado(request):
    
    q = Producto.objects.all()
    contexto = {'datos': q}
    return render(request, 'Vitario/producto/concentrado.html', contexto)

def productoAccesorio(request):
    
    q = Producto.objects.all()
    contexto = {'datos': q}
    return render(request, 'Vitario/producto/accesorio.html', contexto)

def productoMedicamento(request):
    
    q = Producto.objects.all()
    contexto = {'datos': q}
    return render(request, 'Vitario/producto/medicamento.html', contexto)

def productoPremios(request):
    
    q = Producto.objects.all()
    contexto = {'datos': q}
    return render(request, 'Vitario/producto/premio.html', contexto)

# ======================================================================================================================

# ===================================================FACTURA============================================================

"""Toma una solicitud, obtiene todos los objetos del modelo Factura, los pagina, obtiene el número de
    página de la solicitud, obtiene la página del paginador y luego devuelve una representación de la
    página con el objeto de la página como contexto.
    
    :param request: El objeto de la solicitud
    :return: Una lista de objetos.
"""
def factura(request):
    
    q = Factura.objects.all()
    
    p = Paginator(q, 9)
    p_number = request.GET.get('page')
    
    q = p.get_page(p_number)
    
    contexto = {'page_obj': q}
    
    return render(request, 'Vitario/factura/listar_factura.html', contexto)

"""Si la solicitud es una solicitud POST, filtre los objetos Factura por el término de búsqueda, pagine
    los resultados y devuelva los resultados a la plantilla
    
    :param request: El objeto de la solicitud
    :return: un objeto de renderizado.
    """
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
    
"""Toma una solicitud, obtiene todos los productos, usuarios y servicios, y luego presenta la plantilla
    con el contexto.
    
    :param request: El objeto de solicitud utilizado para generar esta respuesta
    :return: la función de renderizado.
"""
def facturaFormulario(request):
    p = Producto.objects.all()
    
    u = Usuario.objects.all()
    
    s = Servicios.objects.all()

    contexto = {'producto':p,'usuario':u,'servicio':s}

    return render(request, 'Vitario/factura/crear_factura.html', contexto)

"""Toma una solicitud, intenta obtener un producto, usuario y servicio, luego, si la solicitud es un
    POST, crea una nueva factura con los datos de la solicitud, la guarda y redirige a la página de la
    factura.
    
    :param request: El objeto de la solicitud
    :return: una redirección a la url 'Vitario:factura'
"""
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

"""Elimina un registro de la base de datos.
    
    :param request: El objeto de la solicitud
    :param id: El id del objeto que se va a eliminar
    :return: una redirección a la url 'Vitario:factura'
"""
def facturaEliminar(request,id):
    try:
        a = Factura.objects.get(pk = id)
        a.delete()
        return redirect('Vitario:factura')
    except Factura.DoesNotExist:
        return HttpResponse('ERROR: factura no encontrado')
    except Exception as e:
        return HttpResponse(f'ERROR: {e}')

"""Obtiene un objeto factura de la base de datos, obtiene todos los productos, usuarios y servicios de
    la base de datos y luego presenta una plantilla con el objeto factura y los demás objetos.
    
    :param request: El objeto de la solicitud
    :param id: el id del objeto a editar
    :return: un objeto de renderizado.
"""
def editarFactura(request, id):
    A = Factura.objects.get(pk = id)

    p = Producto.objects.all()
    
    u = Usuario.objects.all()
    
    s = Servicios.objects.all()

    contexto = {'producto':p,'usuario':u,'servicio':s,"datos":A}

    return render(request, 'Vitario/factura/editar_factura.html', contexto)

"""Toma una solicitud, intenta obtener un objeto de factura con la identificación en la solicitud y
    luego actualiza los campos de ese objeto con los valores en la solicitud
    
    :param request: El objeto de la solicitud
    :return: la función de redirección.
"""
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

# ======================================================================================================================

# ===================================================SERVICIO===========================================================

"""Toma una solicitud, obtiene todos los objetos del modelo de Servicios, los pagina, obtiene el número
    de página de la solicitud, obtiene la página del paginador y luego devuelve una representación de la
    plantilla listar_servicio.html con el objeto de página como contexto.
    
    :param request: El objeto de la solicitud
    :return: Una lista de objetos.
"""
def servicio(request):
    
    q = Servicios.objects.all()
    
    p = Paginator(q, 9)
    p_number = request.GET.get('page')
    
    q = p.get_page(p_number)
    
    contexto = {'page_obj': q}
    
    return render(request, 'Vitario/servicio/listar_servicio.html', contexto)

"""Obtiene todos los objetos del modelo Servicios y los pasa a la plantilla
    
    :param request: El objeto de solicitud es un objeto HttpRequest. Contiene metadatos sobre la
    solicitud, como el método HTTP ("GET" o "POST"), la dirección IP del cliente, los parámetros de
    consulta, etc
    :return: Una lista de objetos.
"""
def servicioTarjetas(request):
    
    q = Servicios.objects.all()
    contexto = {'datos': q}
    return render(request, 'Vitario/servicio/tarjeta_servicio.html', contexto)

"""Si la solicitud es una solicitud POST, filtre el modelo de Servicios por el término de búsqueda,
    pagine los resultados y represente los resultados en una plantilla
    
    :param request: El objeto de la solicitud
    :return: un objeto de renderizado.
"""
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

"""Guarda un archivo en el servidor y luego guarda el nombre del archivo en la base de datos.
    
    :param request: El objeto de la solicitud
    :return: El nombre del archivo.
"""
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

"""Elimina un registro de la base de datos y elimina la imagen del servidor
    
    :param request: El objeto de la solicitud
    :param id: El id del objeto a eliminar
    :return: una redirección a la url vitario:servicio.
"""
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

"""Obtiene el objeto con la clave principal de id del modelo de Servicios y luego lo pasa a la
    plantilla como la variable datos
    
    :param request: El objeto de la solicitud
    :param id: El id del objeto que desea editar
    :return: la plantilla renderizada.
"""
def editarServicio(request, id):
    A = Servicios.objects.get(pk = id)
    contexto = {"datos":A}
    return render(request, 'Vitario/servicio/editar_servicio.html', contexto)

"""Si el método de solicitud es POST, obtenga el objeto con la clave principal igual a la
    identificación enviada en la solicitud POST, si la solicitud tiene un archivo, elimine el archivo
    anterior y guarde el nuevo, luego actualice el objeto con los nuevos datos y redirigir a la página
    de servicio
    
    :param request: El objeto de la solicitud
    :return: la redirección a la url 'Vitario:servicio'
"""
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

# ======================================================================================================================

# ===================================================CITAS==============================================================

"""Toma una solicitud, obtiene todos los objetos del modelo de Citas, los pagina, obtiene el número de
    página de la solicitud, obtiene la página del paginador y luego devuelve una representación de la
    plantilla listar_cita.html con el objeto de página como contexto
    
    :param request: El objeto de la solicitud
    :return: un objeto de renderizado.
"""
def cita(request):
    
    q = Citas.objects.all()
    
    p = Paginator(q, 9)
    p_number = request.GET.get('page')
    
    q = p.get_page(p_number)
    
    contexto = {'page_obj': q}
    
    return render(request, 'Vitario/cita/listar_cita.html', contexto)

"""Si la solicitud es una solicitud POST, filtre los objetos de Citas por el término de búsqueda,
    pagine los resultados y represente los resultados en una plantilla
    
    :param request: El objeto de la solicitud
    :return: un objeto de renderizado.
"""
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

"""Toma una solicitud, obtiene todos los objetos de los modelos Servicios y Usuario, y luego presenta
    la plantilla crear_cita.html con el contexto de los objetos.
    
    :param request: El objeto de solicitud utilizado para generar esta respuesta
    :return: un objeto de renderizado.
"""
def citaFormulario(request):
    p = Servicios.objects.all()
    
    q = Usuario.objects.all()
    
    contexto = {'datos':p,"user":q}
    return render(request, 'Vitario/cita/crear_cita.html',contexto)

"""Toma una solicitud, intenta obtener un servicio y un usuario, luego, si la solicitud es un POST,
    crea una nueva cita con el usuario y el servicio, y la guarda.
    
    :param request: El objeto de la solicitud
    :return: El mensaje de error está siendo devuelto.
"""
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

"""Elimina un registro de la base de datos.
    
    :param request: El objeto de solicitud es un objeto Django que contiene metadatos sobre la solicitud
    enviada al servidor
    :param id: El id del objeto que se va a eliminar
    :return: la respuesta de la solicitud.
"""
def citaEliminar(request,id):
    try:
        a = Citas.objects.get(pk = id)
        a.delete()
        return redirect('Vitario:cita')
    except Citas.DoesNotExist:
        return HttpResponse('ERROR: cita no encontrado')
    except Exception as e:
        return HttpResponse(f'ERROR: {e}')

"""Obtiene los datos de la base de datos y los envía a la plantilla.
    
    :param request: El objeto de la solicitud
    :param id: El id del objeto que desea editar
    :return: Un diccionario con la clave "datos" y el valor A, la clave "usuario" y el valor q, y la
    clave "servi" y el valor b.
"""
def editarCita(request, id):
    A = Citas.objects.get(pk = id)
    
    b = Servicios.objects.all()
    
    q = Usuario.objects.all()
    contexto = {"datos":A,"user":q, "servi":b}
    return render(request, 'Vitario/cita/editar_cita.html', contexto)

"""Toma una solicitud, intenta obtener un objeto Cita con la identificación en la solicitud y luego
    actualiza el objeto con los datos en la solicitud
    
    :param request: El objeto de la solicitud
    :return: la función de redirección.
"""
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
    
def Agendar(request):
    login = request.session.get('logueo', False)
    i = Usuario.objects.get(pk = login[0])
    
    from django.db.models import Count
    q = Disponibilidad.objects.filter(empleado = i).values('fecha_inicio').annotate(dcount=Count('fecha_inicio'))
    # q = Disponibilidad.objects.raw(f"SELECT id, fecha_inicio from Vitario_disponibilidad where empleado_id = {login[0]}  group by fecha_inicio;")
    contexto = {"datos":q}
    return render(request, 'Vitario/cita/listar.html', contexto)

def verAgenda(request, fecha):
    login = request.session.get('logueo', False)
    i = Usuario.objects.get(pk=login[0])
    
    q = Disponibilidad.objects.filter(empleado=i, fecha_inicio=fecha)
    contexto = {"datos":q, "fecha":fecha}
    return render(request, 'Vitario/cita/veragenda.html', contexto)

def guardarAgenda(request, fecha):
    login = request.session.get('logueo', False)
    i = Usuario.objects.get(pk=login[0])
    if request.method == "POST":
        r = Disponibilidad.objects.filter(empleado_id=login[0], fecha_inicio=fecha)
        r.delete()
        for a in request.POST.getlist('agenda[]'):
            tmp = a.split('-')                      
            dia = tmp[0]
            hora = tmp[1]
            print(f"Dia: {dia} - Hora {hora}")
            q = Disponibilidad(empleado=i, dia=dia, hora=hora, fecha_inicio=fecha, fecha_fin=fecha)
            q.save()
    else:
        messages.warning(request, "No se enviaron datos")
    messages.success(request, "Agenda actualizada correctamente!!")
    return redirect('Vitario:veragenda', fecha=fecha)

def apartarCita(request):
    q = Usuario.objects.filter(rol="E")
    contexto = {"datos":q}
    return render(request, 'Vitario/cita/apartar_cita.html', contexto)

def formularioApartarCitas(request, empleado):
    login = request.session.get('logueo', False)
    c = Usuario.objects.get(pk=login[0])
    
    fecha = datetime.now()
    fecha = f"{fecha.year}-{fecha.month}-01"
    print(fecha)
    
    q = Disponibilidad.objects.filter(empleado=empleado, fecha_inicio=fecha)
    contexto = {"datos":q, "fecha":fecha}
    return render(request, 'Vitario/cita/vista_apartar_cita.html', contexto)

def carritoCompra(request):
    return render(request, 'Vitario/carrito/carrito.html')

def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.agregar(producto)
    return redirect('Vitario:carrito')

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect('Vitario:carrito')

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect('Vitario:carrito')

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect('Vitario:carrito')

# ======================================================================================================================