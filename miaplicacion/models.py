from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Rol(models.Model):
    nombre=models.CharField(max_length=255, blank=False, unique=True)

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    talle = models.CharField(max_length=100)
    cantidad_disponible = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"Producto:{self.nombre}"

class Modelo(models.Model):
   producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
   codigo = models.CharField(max_length=100)
   nombre = models.CharField(max_length=100)

class Encargues(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha=models.DateField()
    cantidadproducto=models.IntegerField()
    def __str__(self):
        return f"{self.producto.nombre}"

class Encargado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.IntegerField()
    direccion = models.CharField(max_length=100)
    def __str__(self):
        return f"Encargado:{self.nombre}"

class Cliente(AbstractUser):
    nombre = models.CharField(max_length=100)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.rol_id:
            # Asigna un rol por defecto si no se asignó ninguno
            self.rol = Rol.objects.get_or_create(nombre='Administrador')[0]
        super().save(*args, **kwargs) 

class Persona(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='persona')
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    dni = models.CharField(max_length=11)

class Comercio(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='comercio')
    rut = models.CharField(max_length=11)
    encargue = models.OneToOneField(Encargues, on_delete=models.CASCADE)

class CompraPersona(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    cantidadS = models.PositiveIntegerField()
    factura = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

class CompraComercio(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    cantidadS = models.PositiveIntegerField()
    factura = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

class Tienda(models.Model):
    nombre=models.CharField(max_length=100)
    class Meta:
        abstract = True # Indico que la clase será de tipo abstacta, no tendrá una tabla en la BD.

class Sucursal(Tienda):
    direccion = models.CharField(max_length=100)
    telefono = models.IntegerField()
    encargado = models.OneToOneField(Encargado, on_delete=models.CASCADE)

class TiendaVirtual(Tienda):
    url=models.URLField(max_length=100)
    encargado = models.OneToOneField(Encargado, on_delete=models.CASCADE)

class TiendaMovil(Tienda):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    matricula = models.CharField(max_length=100)
    encargado = models.OneToOneField(Encargado, on_delete=models.CASCADE)


