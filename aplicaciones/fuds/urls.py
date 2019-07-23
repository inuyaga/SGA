from django.contrib import admin
from django.urls import path
from aplicaciones.inicio.views import inicio, err_permisos
from aplicaciones.fuds.views import MotivoCreate, MotivoUpdate, MotivoList, MotivoDelete,\
ConformidadCreate,ConformidadUpdate,ConformidadList,ConformidadDelete,\
ZonaCreate,ZonaList,ZonaUpdate,ZonaDelete,\
VendedorCreate,VendedorList, VendedorUpdate,VendedorDelete,\
FudCreate, FudList, FudUpdate, FudDelete,\
PartidaCreate, PartidaView, \
TramiteCreate,TramiteUpdate,TramiteDelete,TramiteList, \
ClientCreate,ClientUpdate,ClientList,ClientDelete

app_name = "fuds"
urlpatterns = [
    path('NuevoMotivo/', MotivoCreate.as_view(), name='NuevoMotivo'),
    path('EditarMotivo/<int:pk>/', MotivoUpdate.as_view(), name='EditarMotivo'),
    path('ListarMotivo/', MotivoList.as_view(), name='ListarMotivo'),
    path('EliminarMotivo/<int:pk>/', MotivoDelete.as_view(), name='EliminarMotivo'),
    
    path('NuevaConformidad/', ConformidadCreate.as_view(), name='NuevaConformidad'),
    path('EditarConformidad/<int:pk>/', ConformidadUpdate.as_view(), name='EditarConformidad'),
    path('ListarConformidad/', ConformidadList.as_view(), name='ListarConformidad'),
    path('EliminarConformidad/<int:pk>/', ConformidadDelete.as_view(), name='EliminarConformidad'),

    path('NuevoCliente/', ClientCreate.as_view(), name='NuevoCliente'),
    path('EditarCliente/<int:pk>/', ClientUpdate.as_view(), name='EditarCliente'),
    path('ListarClientes/', ClientList.as_view(), name='ListarClientes'),
    path('EliminarCliente/<int:pk>/', ClientDelete.as_view(), name='EliminarCliente'),

    path('NuevoTramite/', TramiteCreate.as_view(), name='NuevoTramite'),
    path('EditarTramite/<int:pk>/', TramiteUpdate.as_view(), name='EditarTramite'),
    path('ListarTramites/', TramiteList.as_view(), name='ListarTramites'),
    path('EliminarTramite/<int:pk>/', TramiteDelete.as_view(), name='EliminarTramite'),

    path('NuevaZona/', ZonaCreate.as_view(), name='NuevaZona'),
    path('EditarZona/<int:pk>/', ZonaUpdate.as_view(), name='EditarZona'),
    path('ListarZona/', ZonaList.as_view(), name='ListarZona'),
    path('EliminarZona/<int:pk>/', ZonaDelete.as_view(), name='EliminarZona'),

    path('NuevoVendedor/', VendedorCreate.as_view(), name='NuevoVendedor'),
    path('ListarVendedor/', VendedorList.as_view(), name='ListarVendedor'),
    path('EditarVendedor/<int:pk>/', VendedorUpdate.as_view(), name='EditarVendedor'),
    path('EliminarVendedor/<int:pk>/', VendedorDelete.as_view(), name='EliminarVendedor'),

    path('nuevo_fud/', FudCreate.as_view(), name='fud_create'),
    path('list/fud/', FudList.as_view(), name='fud_list'),
    path('update/fud/<int:pk>/', FudUpdate.as_view(), name='fud_update'),
    path('eliminar/fud/<int:pk>/', FudDelete.as_view(), name='fud_delete'),

    path('Partida/<int:pk>/', PartidaCreate.as_view(), name='Partida'),
    path('PartidaSearch/', PartidaView.as_view(), name='PartidaSearch'),

    path('FudSearch/', PartidaView.as_view(), name='FudSearch'),

    path('permisos/', err_permisos, name='need_permisos'),
]