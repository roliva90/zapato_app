from django.urls import path
from .import views
from miaplicacion import views


urlpatterns=[
    path('',views.index, name='index'),
    
    path('personas',views.listar_personas,name='listar_personas'),
    
    path('productos',views.listar_productos,name='listar_productos'),
    path('productos/crear/',views.crear_productos,name='crear_productos'),
    path('productos/editar/<int:pk>/',views.editar_productos,name='editar_productos'),
    path('productos/eliminar/<int:pk>/',views.eliminar_productos,name='eliminar_productos'),
    
    path('modelo',views.listar_modelos,name='listar_modelos'),
    path('modelo/crear/',views.crear_modelos,name='crear_modelos'),
    path('modelo/editar/<int:pk>/',views.editar_modelos,name='editar_modelos'),
    path('modelo/eliminar/<int:pk>/',views.eliminar_modelos,name='eliminar_modelos'),
    
    path('encargue',views.listar_encargues,name='listar_encargues'),
    path('encargue/crear/',views.crear_encargues,name='crear_encargues'),
    path('encargue/editar/<int:pk>/',views.editar_encargues,name='editar_encargues'),
    path('encargue/eliminar/<int:pk>/',views.eliminar_encargues,name='eliminar_encargues'),
    
    path('comercio/',views.listar_comercios,name='listar_comercios'),
    
    path('encargado',views.listar_encargados,name='listar_encargados'),
    path('encargado/crear/',views.crear_encargados,name='crear_encargados'),
    path('encargado/editar/<int:pk>/',views.editar_encargados,name='editar_encargados'),
    path('encargado/eliminar/<int:pk>/',views.eliminar_encargados,name='eliminar_encargados'), 
    
    path('compracomercio',views.listar_compracomercios,name='listar_compracomercios'),
    path('compracomercio/crear/<int:producto_id>/',views.compra_comercio,name='compra_comercio'),
    path('compracomercio/eliminar/<int:pk>/',views.eliminar_compracomercios,name='eliminar_compracomercios'),
    
    path('tiendavirtual',views.listar_tiendavirtual,name='listar_tiendavirtual'),
    path('tiendavirtual/crear/',views.crear_tiendavirtual,name='crear_tiendavirtual'),
    path('tiendavirtual/editar/<int:pk>/',views.editar_tiendavirtual,name='editar_tiendavirtual'),
    path('tiendavirtual/eliminar/<int:pk>/',views.eliminar_tiendavirtual,name='eliminar_tiendavirtual'), 
    
    path('sucursal',views.listar_sucursal,name='listar_sucursal'),
    path('sucursal/crear/',views.crear_sucursal,name='crear_sucursal'),
    path('sucursal/editar/<int:pk>/',views.editar_sucursal,name='editar_sucursal'),
    path('sucursal/eliminar/<int:pk>/',views.eliminar_sucursal,name='eliminar_sucursal'), 
    
    path('tiendamovil',views.listar_tiendamovil,name='listar_tiendamovil'),
    path('tiendamovil/crear/',views.crear_tiendamovil,name='crear_tiendamovil'),
    path('tiendamovil/editar/<int:pk>/',views.editar_tiendamovil,name='editar_tiendamovil'),
    path('tiendamovil/eliminar/<int:pk>/',views.eliminar_tiendamovil,name='eliminar_tiendamovil'),
    
    path('roles/', views.listar_roles, name='listar_roles'),
    path('roles/crear/', views.crear_rol, name='crear_rol'),
    path('roles/editar/<int:pk>/', views.editar_rol,name='editar_rol'),
    path('roles/eliminar/<int:pk>/',views.eliminar_rol, name='eliminar_rol'),

    path('comprapersona',views.listar_comprapersonas,name='listar_comprapersonas'),
    path('comprapersona/crear/<int:producto_id>/',views.compra_persona,name='compra_persona'),
    path('comprapersona/eliminar/<int:pk>/',views.eliminar_comprapersonas,name='eliminar_comprapersonas'),

    
    path('account/login/', views.iniciar_sesion, name='login'),
    path('accounts/logout/', views.cerrar_sesion, name='logout'),
    # URL Acceso Denegado
    path('acceso_denegado/', views.acceso_denegado, name='acceso_denegado'),
     # URL Cambio de Contraseña
    path('cambiar_contraseña/', views.cambiar_contraseña, name='cambiar_contraseña'),

    
    path('clientes/crear/', views.register_view, name='register'),  # Cambiar 'clientes' por 'clientes/registrar'
    path('clientes/', views.client_list_view, name='listar_clientes'),
    path('clientes/eliminar/<int:client_id>/', views.delete_client_view, name='delete_client'),
    path('clientes/editar/<int:cliente_id>/', views.edit_view, name='edit_client'),
]