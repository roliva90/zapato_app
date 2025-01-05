from django.shortcuts import redirect, render, get_object_or_404, HttpResponse
from django.contrib.auth.views import LoginView
from .decorators import role_required
from django.db import IntegrityError
from .models import (
    Persona,
    Producto,
    Modelo,
    Encargado,
    Encargues,
    Comercio,
    TiendaMovil,
    TiendaVirtual,
    Sucursal,
    CompraComercio,
    CompraPersona,
    Rol,
    Cliente,
)
from .forms import (
    ClienteForm,
    ClienteEditForm,
    PersonaForm,
    ProductoForm,
    ModeloForm,
    EncargadoForm,
    EncarguesForm,
    ComercioForm,
    CompraComercioForm,
    CustomUserCreationForm,
    TiendaMovilForm,
    TiendaVirtualForm,
    SucursalForm,
    RolForm,
    CompraPersonaForm,ClientePasswordForm
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
@login_required
@role_required(['Administrador','Persona','Comercio'])
def index(request):
    return render(request, "base.html")

# Vista de Acceso Denegado
@login_required
def acceso_denegado(request):
    return render(request, 'acceso_denegado.html')

# Autenticación LOGIN y LOGOUT
def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
@role_required(['Administrador','Persona','Comercio'])
def cerrar_sesion(request):
    logout(request)
    return redirect('index')

# Modificar Contraseña
@login_required
@role_required('Administrador')
def cambiar_contraseña(request):
    if request.method == 'POST':
        form = ClientePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contraseña cambiada con éxito. Por favor, vuelve a iniciar sesión.')
            logout(request)
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                label = form.fields[field].label
                for error in errors:
                    messages.error(request, f'Error en "{label}": {error}')
            return render(request, 'cambiar_contraseña.html', {'form': form})
    else:
        form = ClientePasswordForm(user=request.user)

    return render(request, 'cambiar_contraseña.html', {'form': form})


# CRUD PERSONA
@login_required
@role_required(['Administrador','Persona','Comercio'])
def listar_personas(request):
    personas = Persona.objects.all()
    return render(request, "personas/listar.html", {"personas": personas})


# CRUD PRODUCTOS
@login_required
@role_required(['Administrador','Persona','Comercio'])
def listar_productos(request):
    productos = Producto.objects.all()
    success_message = request.session.pop('success_message', None)
    return render(request, "productos/listar.html", {"productos": productos})

@login_required
@role_required('Administrador')
def crear_productos(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado con éxito.")
        return redirect("listar_productos")
    else:
        form = ProductoForm()
    return render(request, "productos/crear.html", {"form": form})

@login_required
@role_required('Administrador')
def editar_productos(request, pk):
    productos = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=productos)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto Actualizado con éxito.")
        return redirect("listar_productos")
    else:
        form = ProductoForm(instance=productos)
    return render(request, "productos/editar.html", {"form": form})

@login_required
@role_required('Administrador')
def eliminar_productos(request, pk):
    productos = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        productos.delete()
        messages.success(request, "Producto eliminado con éxito.")
        return redirect("listar_productos")
    return render(request, "productos/eliminar.html", {"producto": productos})


# CRUD MODELOS
@login_required
@role_required(['Administrador','Persona','Comercio'])
def listar_modelos(request):
    modelos = Modelo.objects.all()
    return render(request, "modelo/listar.html", {"modelos": modelos})

@login_required
@role_required('Administrador')
def crear_modelos(request):
    productos = Producto.objects.all()
    if request.method == "POST":
        form = ModeloForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Modelo creado con éxito.")
        return redirect("listar_modelos")
    else:
        form = ModeloForm()
    return render(request, "modelo/crear.html", {"form": form, "productos": productos})

@login_required
@role_required('Administrador')
def editar_modelos(request, pk):
    modelos = get_object_or_404(Modelo, pk=pk)
    if request.method == "POST":
        form = ModeloForm(request.POST, instance=modelos)
        if form.is_valid():
            form.save()
            messages.success(request, "Modelo Actualizado con éxito.")
        return redirect("listar_modelos")
    else:
        form = ModeloForm(instance=modelos)
    return render(request, "modelo/editar.html", {"form": form})

@login_required
@role_required('Administrador')
def eliminar_modelos(request, pk):
    modelos = get_object_or_404(Modelo, pk=pk)
    if request.method == "POST":
        modelos.delete()
        messages.success(request, "Modelo eliminado con éxito.")
        return redirect("listar_modelos")
    return render(request, "modelo/eliminar.html", {"modelos": modelos})


# CRUD ENCARGUE
@login_required
@role_required('Administrador')
def listar_encargues(request):
    encargues = Encargues.objects.all()
    return render(request, "encargue/listar.html", {"encargues": encargues})

@login_required
@role_required('Administrador')
def crear_encargues(request):
    productos = Producto.objects.all()
    if request.method == "POST":
        form = EncarguesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Encargue creado con éxito.")
        return redirect("listar_encargues")
    else:
        form = EncarguesForm()
    return render(
        request, "encargue/crear.html", {"form": form, "productos": productos}
    )

@login_required
@role_required('Administrador')
def editar_encargues(request, pk):
    encargues = get_object_or_404(Encargues, pk=pk)
    if request.method == "POST":
        form = EncarguesForm(request.POST, instance=encargues)
        if form.is_valid():
            form.save()
            messages.success(request, "Encargue Actualizado con éxito.")
        return redirect("listar_encargues")
    else:
        form = EncarguesForm(instance=encargues)
    return render(request, "encargue/editar.html", {"form": form})

@login_required
@role_required('Administrador')
def eliminar_encargues(request, pk):
    encargues = get_object_or_404(Encargues, pk=pk)
    if request.method == "POST":
        encargues.delete()
        messages.success(request, "Encargue Eliminado con éxito.")
        return redirect("listar_encargues")
    return render(request, "encargue/eliminar.html", {"encargues": encargues})


# CRUD COMERCIO
@login_required
@role_required(['Administrador','Comercio'])
def listar_comercios(request):
    comercios = Comercio.objects.all()
    return render(request, "comercio/listar.html", {"comercios": comercios})


# CRUD ENCARGADO
@login_required
@role_required('Administrador')
def listar_encargados(request):
    encargados = Encargado.objects.all()
    return render(request, "encargado/listar.html", {"encargados": encargados})

@login_required
@role_required('Administrador')
def crear_encargados(request):
    if request.method == "POST":
        form = EncargadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Encargado creado con éxito.")
        return redirect("listar_encargados")
    else:
        form = EncargadoForm()
    return render(request, "encargado/crear.html", {"form": form})

@login_required
@role_required('Administrador')
def editar_encargados(request, pk):
    encargados = get_object_or_404(Encargado, pk=pk)
    if request.method == "POST":
        form = EncargadoForm(request.POST, instance=encargados)
        if form.is_valid():
            form.save()
            messages.success(request, "Encargado Actualizado con éxito.")
        return redirect("listar_encargados")
    else:
        form = EncargadoForm(instance=encargados)
    return render(request, "encargado/editar.html", {"form": form})

@login_required
@role_required('Administrador')
def eliminar_encargados(request, pk):
    encargados = get_object_or_404(Encargado, pk=pk)
    if request.method == "POST":
        encargados.delete()
        messages.success(request, "Encargado eliminado con éxito.")
        return redirect("listar_encargados")
    return render(request, "encargado/eliminar.html", {"encargados": encargados})


# CRUD COMPRACOMERCIO
@login_required
@role_required('Administrador')
def listar_compracomercios(request):
    compracomercios = CompraComercio.objects.all()
    return render(
        request, "compracomercio/listar.html", {"compracomercios": compracomercios}
    )

@login_required
@role_required('Comercio')
def compra_comercio(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        form = CompraComercioForm(request.POST)
        if form.is_valid():
            compra_comercio = form.save(commit=False)

            if compra_comercio.cantidadS > producto.cantidad_disponible:
                messages.error(request, 'La cantidad solicitada excede la cantidad disponible.')
                return redirect('compra_comercio', producto_id=producto_id)
            
            compra_comercio.cliente = request.user
            compra_comercio.monto = compra_comercio.cantidadS * producto.precio
            producto.cantidad_disponible -= compra_comercio.cantidadS
            producto.save()
            compra_comercio.save()
            
            messages.success(request, '¡Solicitud realizada con éxito!')
            return redirect('listar_productos')
    
    else:
        form = CompraComercioForm()

    return render(request, 'compracomercio/crear.html', {'form': form, 'producto': producto, 'precio_producto': producto.precio})

@login_required
@role_required('Administrador')
def eliminar_compracomercios(request, pk):
    compracomercios = get_object_or_404(CompraComercio, pk=pk)
    if request.method == "POST":
        compracomercios.delete()
        return redirect("listar_compracomercios")
    return render(
        request, "compracomercio/eliminar.html", {"compracomercios": compracomercios}
    )

# CRUD COMPRAPERSONA
@login_required
@role_required('Administrador')
def listar_comprapersonas(request):
    comprapersonas = CompraPersona.objects.all()
    return render(
        request, "comprapersona/listar.html", {"comprapersonas": comprapersonas}
    )

@login_required
@role_required('Persona')
def compra_persona(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        form = CompraPersonaForm(request.POST)
        if form.is_valid():
            compra_persona= form.save(commit=False)

            if compra_persona.cantidadS > producto.cantidad_disponible:
                messages.error(request, 'La cantidad solicitada excede la cantidad disponible.')
                return redirect('compra_persona', producto_id=producto_id)
            
            compra_persona.cliente = request.user
            compra_persona.monto = compra_persona.cantidadS * producto.precio
            producto.cantidad_disponible -= compra_persona.cantidadS
            producto.save()
            compra_persona.save()
            
            messages.success(request, '¡Solicitud realizada con éxito!')
            return redirect('listar_productos')
    
    else:
        form = CompraPersonaForm()

    return render(request, 'comprapersona/crear.html', {'form': form, 'producto': producto, 'precio_producto': producto.precio})

@login_required
@role_required('Administrador')
def eliminar_comprapersonas(request, pk):
    comprapersonas = get_object_or_404(CompraPersona, pk=pk)
    if request.method == "POST":
        comprapersonas.delete()
        return redirect("listar_comprapersonas")
    return render(
        request, "comprapersona/eliminar.html", {"comprapersonas": comprapersonas}
    )

#CRUD  TIENDA VIRTUAL
@login_required
@role_required('Administrador')
def listar_tiendavirtual(request):
    tiendavirtual = TiendaVirtual.objects.all()
    return render(request, "tiendavirtual/listar.html", {"tiendavirtual": tiendavirtual})

@login_required
@role_required('Administrador')
def crear_tiendavirtual(request):
    encargados = Encargado.objects.all()
    if request.method == "POST":
        form = TiendaVirtualForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tienda Virtual creada con éxito.")
        return redirect("listar_tiendavirtual")
    else:
        form = TiendaVirtualForm()
    return render(
        request, "tiendavirtual/crear.html", {"form": form, "encargados": encargados}
    )

@login_required
@role_required('Administrador')
def editar_tiendavirtual(request, pk):
    encargados = Encargado.objects.all()
    tiendavirtual = get_object_or_404(TiendaVirtual, pk=pk)
    if request.method == "POST":
        form = TiendaVirtualForm(request.POST, instance=tiendavirtual)
        if form.is_valid():
            form.save()
            messages.success(request, "Tienda Virtual Actualizada con éxito.")
        return redirect("listar_tiendavirtual")
    else:
        form = TiendaVirtualForm(instance=tiendavirtual)
    return render(
        request, "tiendavirtual/editar.html", {"form": form, "encargados": encargados}
    )

@login_required
@role_required('Administrador')
def eliminar_tiendavirtual(request, pk):
    tiendavirtual = get_object_or_404(TiendaVirtual, pk=pk)
    if request.method == "POST":
        tiendavirtual.delete()
        messages.success(request, "Tienda Virtual eliminada con éxito.") 
        return redirect("listar_tiendavirtual")
    return render(request, "tiendavirtual/eliminar.html", {"tiendavirtual": tiendavirtual})

# CRUD SUCURSAL
@login_required
@role_required('Administrador')
def listar_sucursal(request):
    sucursal = Sucursal.objects.all()
    return render(request, "sucursal/listar.html", {"sucursales": sucursal})

@login_required
@role_required('Administrador')
def crear_sucursal(request):
    encargados = Encargado.objects.all()
    if request.method == "POST":
        form = SucursalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sucursal creada con éxito.") 
        return redirect("listar_sucursal")
    else:
        form = SucursalForm()
    return render(
        request, "sucursal/crear.html", {"form": form, "encargados": encargados}
    )

@login_required
@role_required('Administrador')
def editar_sucursal(request, pk):
    encargados = Encargado.objects.all()
    sucursal = get_object_or_404(Sucursal, pk=pk)
    if request.method == "POST":
        form = SucursalForm(request.POST, instance=sucursal)
        if form.is_valid():
            form.save()
            messages.success(request, "Sucursal Actualizada con éxito.") 
        return redirect("listar_sucursal")
    else:
        form = SucursalForm(instance=sucursal)
    return render(
        request, "sucursal/editar.html", {"form": form, "encargados": encargados}
    )

@login_required
@role_required('Administrador')
def eliminar_sucursal(request, pk):
    sucursal = get_object_or_404(Sucursal, pk=pk)
    if request.method == "POST":
        sucursal.delete()
        messages.success(request, "Sucursal eliminada con éxito.") 
        return redirect("listar_sucursal")
    return render(request, "sucursal/eliminar.html", {"sucursales": sucursal})


# CRUD TIENDAMOVIL
@login_required
@role_required('Administrador')
def listar_tiendamovil(request):
    tiendamovil = TiendaMovil.objects.all()
    return render(request, "tiendamovil/listar.html", {"tiendamovil": tiendamovil})

@login_required
@role_required('Administrador')
def crear_tiendamovil(request):
    encargados = Encargado.objects.all()
    if request.method == "POST":
        form = TiendaMovilForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tienda Movil creada con éxito.") 
        return redirect("listar_tiendamovil")
    else:
        form = TiendaMovilForm()
    return render(
        request, "tiendamovil/crear.html", {"form": form, "encargados": encargados}
    )

@login_required
@role_required('Administrador')
def editar_tiendamovil(request, pk):
    encargados = Encargado.objects.all()
    tiendamovil = get_object_or_404(TiendaMovil, pk=pk)
    if request.method == "POST":
        form = TiendaMovilForm(request.POST, instance=tiendamovil)
        if form.is_valid():
            form.save()
            messages.success(request, "Tienda Movil Actualizada con éxito.") 
        return redirect("listar_tiendamovil")
    else:
        form = TiendaMovilForm(instance=tiendamovil)
    return render(
        request, "tiendamovil/editar.html", {"form": form, "encargados": encargados}
    )

@login_required
@role_required('Administrador')
def eliminar_tiendamovil(request, pk):
    tiendamovil = get_object_or_404(TiendaMovil, pk=pk)
    if request.method == "POST":
        tiendamovil.delete()
        messages.success(request, "Tienda Movil eliminada con éxito.") 
        return redirect("listar_tiendamovil")
    return render(request, "tiendamovil/eliminar.html", {"tiendamovil": tiendamovil})


# CRUD ROL
@login_required
@role_required('Administrador')
def listar_roles(request):
    roles = Rol.objects.all()
    success_message = request.session.pop("success_message", None)
    return render(
        request, "roles/listar.html", {"rol": roles, "success_message": success_message}
    )

@login_required
@role_required('Administrador')
def crear_rol(request):
    if request.method == "POST":
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            request.session["success_message"] = "¡Rol insertado correctamente!"
            return redirect("listar_roles")
        else:
            for field, errors in form.errors.items():
                label = form.fields[field].label
                for error in errors:
                    messages.error(request, f'Error en "{label}": {error}')
    else:
        form = RolForm()
    return render(request, "roles/crear.html", {"form": form})

@login_required
@role_required('Administrador')
def editar_rol(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    if request.method == "POST":
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            form.save()
            request.session["success_message"] = "¡Datos actualizados correctamente!"
            return redirect("listar_roles")
        else:
            for field, errors in form.errors.items():
                label = form.fields[field].label
                for error in errors:
                    messages.error(request, f'Error en "{label}": {error}')
            return render(request, "roles/editar.html", {"form": form})
    else:
        form = RolForm(instance=rol)
    return render(request, "roles/editar.html", {"form": form})

@login_required
@role_required('Administrador')
def eliminar_rol(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    if request.method == "POST":
        rol.delete()
        return redirect("listar_roles")
    return render(request, "roles/eliminar.html", {"rol": rol})

@login_required
@role_required('Administrador')
def client_list_view(request):
    clientes = (
        Cliente.objects.select_related("rol")
        .prefetch_related("persona", "comercio")
        .all()
    )
    return render(request, "clientes/listar.html", {"clientes": clientes})

@login_required
@role_required('Administrador')
def register_view(request):
    # Asegúrate de que los roles existan en la base de datos
    try:
        persona_role, created = Rol.objects.get_or_create(nombre="Persona")
        comercio_role, created = Rol.objects.get_or_create(nombre="Comercio")
    except IntegrityError:
        # En caso de algún problema con la base de datos, puedes manejarlo aquí
        return render(
            request,
            "clientes/register.html",
            {
                "error_message": "Error al verificar los roles necesarios. Contacte con el administrador.",
            }
        )

    if request.method == "POST":
        cliente_form = ClienteForm(request.POST)
        rol_id = request.POST.get("rol")  # Obtener el ID del rol

        persona_form = None
        comercio_form = None

        if cliente_form.is_valid():
            cliente = cliente_form.save(commit=False)
            cliente.set_password(request.POST["password1"])

            # Obtener la instancia del rol usando el ID
            try:
                rol = Rol.objects.get(id=rol_id)
                cliente.rol = rol
            except Rol.DoesNotExist:
                return render(
                    request,
                    "register.html",
                    {
                        "cliente_form": cliente_form,
                        "persona_form": persona_form,
                        "comercio_form": comercio_form,
                        "roles": Rol.objects.all(),
                        "encargues": Encargues.objects.all(),
                        "persona_role_id": persona_role.id,
                        "comercio_role_id": comercio_role.id,
                        "error_message": "Rol no encontrado."
                    }
                )

            cliente.save()

            if rol.nombre == "Persona":
                persona_form = PersonaForm(request.POST)
                if persona_form.is_valid():
                    persona = persona_form.save(commit=False)
                    persona.cliente = cliente
                    persona.save()

            elif rol.nombre == "Comercio":
                comercio_form = ComercioForm(request.POST)
                if comercio_form.is_valid():
                    comercio = comercio_form.save(commit=False)
                    comercio.cliente = cliente
                    comercio.save()

            return redirect("listar_clientes")

    else:
        cliente_form = ClienteForm()
        persona_form = PersonaForm()
        comercio_form = ComercioForm()

    return render(
        request,
        "clientes/register.html",
        {
            "cliente_form": cliente_form,
            "persona_form": persona_form,
            "comercio_form": comercio_form,
            "roles": Rol.objects.all(),
            "encargues": Encargues.objects.all(),
            "persona_role_id": persona_role.id,
            "comercio_role_id": comercio_role.id,
        },
    )
@login_required
@role_required('Administrador')
def edit_view(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    rol = cliente.rol

    # Inicializar formularios a None por defecto
    persona_form = None
    comercio_form = None
    encargues = None  # Inicializa encargues como None

    if request.method == "POST":
        cliente.nombre = request.POST.get("nombre")
        cliente.email = request.POST.get("email")
        cliente.save()

        if rol.nombre == "Persona":
            persona = get_object_or_404(Persona, cliente=cliente)
            persona.apellidos = request.POST.get("apellidos")
            persona.telefono = request.POST.get("telefono")
            persona.dni = request.POST.get("dni")
            persona.save()

        elif rol.nombre == "Comercio":
            comercio = get_object_or_404(Comercio, cliente=cliente)
            comercio.rut = request.POST.get("rut")
            encargo_id = request.POST.get("encargue")
            if encargo_id:
                encargo = get_object_or_404(Encargues, id=encargo_id)
                comercio.encargue = encargo
            else:
                comercio.encargue = None
            comercio.save()

        return redirect("listar_clientes")
    
    else:
        if rol.nombre == "Persona":
            persona_form = cliente.persona
            comercio_form = None
        elif rol.nombre == "Comercio":
            comercio_form = cliente.comercio
            persona_form = None
            encargues = Encargues.objects.all()

    return render(
        request,
        "clientes/editar.html",
        {
            "cliente": cliente,
            "persona_form": persona_form,
            "comercio_form": comercio_form,
            "encargues": encargues if rol.nombre == "Comercio" else None,
        },
    )

@login_required
@role_required('Administrador')
def delete_client_view(request, client_id):
    cliente = get_object_or_404(Cliente, pk=client_id)
    cliente.delete()
    messages.success(request, "Cliente eliminado exitosamente.")
    return redirect("listar_clientes")