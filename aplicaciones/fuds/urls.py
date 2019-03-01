from django.contrib import admin
from django.urls import path
from aplicaciones.inicio.views import inicio, err_permisos
from aplicaciones.fuds.views import MotivoCreate, MotivoUpdate, MotivoList, MotivoDelete,\
    ConformidadCreate,ConformidadUpdate,ConformidadList,ConformidadDelete,\
    FudCreate, FudList,\
    FacturaCreate,FacturaDelete,FacturaList,FacturaUpdate

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
    
    path('NuevaFactura/', FacturaCreate.as_view(), name='NuevaFactura'),
    path('EditarFactura/<int:pk>/', FacturaUpdate.as_view(), name='EditarFactura'),
    path('ListarFactura/', FacturaList.as_view(), name='ListarFacturas'),
    path('EliminarFactura/<int:pk>/', FacturaDelete.as_view(), name='EliminarFactura'),
    path('permisos/', err_permisos, name='need_permisos'),

    path('nuevo_fud/', FudCreate.as_view(), name='fud_create'),
    path('list/fud/', FudList.as_view(), name='fud_list'),
    path('update/fud/', FudList.as_view(), name='fud_update'),
    path('delete/fud/', FudList.as_view(), name='fud_delete'),
]