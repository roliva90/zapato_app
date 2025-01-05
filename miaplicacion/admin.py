from django.contrib import admin
from .models import Persona,Producto,CompraPersona,CompraComercio,Comercio,Modelo,Tienda,TiendaMovil,TiendaVirtual,Encargado,Encargues,Sucursal,Cliente

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre','color','talle')
    search_fields = ('nombre',)
admin.site.register (Producto, ProductoAdmin)    

class ModeloAdmin(admin.ModelAdmin):
    list_display = ('producto','codigo','nombre')
    search_fields = ('producto',)
admin.site.register (Modelo, ModeloAdmin)   

class ComercioAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'rut', 'encargue')

    def cliente_nombre(self, obj):
        return obj.cliente.nombre
    cliente_nombre.short_description = 'Nombre del Cliente'

    list_display = ('cliente_nombre', 'rut', 'encargue') 

'''class CompraComercioAdmin(admin.ModelAdmin):
    list_display = ('comercio','factura','monto','fecha')
    search_fields = ('comercio',)
admin.site.register (CompraComercio,CompraComercioAdmin)'''

# Register your models here.
admin.site.register(Persona),
#admin.site.register(Producto),
#admin.site.register(Modelo),
admin.site.register(Encargado),
admin.site.register(Encargues),
#admin.site.register(Comercio),
#admin.site.register(CompraComercio),
admin.site.register(CompraPersona),
admin.site.register(TiendaMovil),
admin.site.register(Sucursal),
admin.site.register(TiendaVirtual),
admin.site.register(Cliente),