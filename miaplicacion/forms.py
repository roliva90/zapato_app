from django import forms
from .models import Cliente,Persona,Producto,Comercio,CompraComercio,CompraPersona,Encargado,Encargues,Modelo,Sucursal,TiendaMovil,TiendaVirtual,Rol
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth.models import User

class ClienteForm(UserCreationForm):
    rol = forms.ModelChoiceField(queryset=Rol.objects.all(), required=True)

    class Meta:
        model = Cliente
        fields = ['username', 'email', 'password1', 'password2', 'nombre', 'rol']

class ClienteEditForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'email']

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['apellidos', 'telefono', 'dni']

class ProductoForm(forms.ModelForm):
    class Meta:
        model=Producto
        fields=['nombre','color','talle', 'cantidad_disponible', 'precio']

class ModeloForm(forms.ModelForm):
    class Meta:
        model=Modelo
        fields=['codigo','nombre','producto']

class EncarguesForm(forms.ModelForm):
    class Meta:
        model=Encargues
        fields=['producto','fecha','cantidadproducto']
      
class EncargadoForm(forms.ModelForm):
    class Meta:
        model=Encargado
        fields=['nombre','apellido','telefono','direccion']

class ComercioForm(forms.ModelForm):
    class Meta:
        model = Comercio
        fields = ['rut', 'encargue']    

class CompraComercioForm(forms.ModelForm):
    class Meta:
        model = CompraComercio
        fields = ['producto', 'cantidadS', 'factura', 'monto']

    def clean(self):
        cleaned_data = super().clean()
        cantidad_solicitada = cleaned_data.get("cantidadS")
        producto = cleaned_data.get("producto")

        if producto and cantidad_solicitada:
            if cantidad_solicitada > producto.cantidad_disponible:
                raise forms.ValidationError(f'La cantidad solicitada excede la cantidad disponible de {producto.nombre}.')
        
        return cleaned_data     

class CompraPersonaForm(forms.ModelForm):
    class Meta:
        model = CompraPersona
        fields = ['producto', 'cantidadS', 'factura', 'monto']

    def clean(self):
        cleaned_data = super().clean()
        cantidad_solicitada = cleaned_data.get("cantidadS")
        producto = cleaned_data.get("producto")

        if producto and cantidad_solicitada:
            if cantidad_solicitada > producto.cantidad_disponible:
                raise forms.ValidationError(f'La cantidad solicitada excede la cantidad disponible de {producto.nombre}.')
        
        return cleaned_data   

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', "first_name", "last_name", "email", "password1", "password2"]

class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = ['nombre', 'direccion', 'telefono', 'encargado']

class TiendaVirtualForm(forms.ModelForm):
    class Meta:
        model = TiendaVirtual
        fields = ['nombre', 'url', 'encargado']

class TiendaMovilForm(forms.ModelForm):
    class Meta:
        model = TiendaMovil
        fields = ['nombre', 'marca', 'modelo', 'matricula', 'encargado']

class RolForm(forms.ModelForm):
    class Meta:
        model=Rol
        fields=['nombre']

# FORMULARIO de Cambio de Contraseña
class ClientePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Contraseña actual",
        widget=forms.PasswordInput(), 
        required=True
    )
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(),
        required=True
    )
    new_password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput(),
        required=True
    )