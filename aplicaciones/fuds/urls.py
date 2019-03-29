from django.contrib import admin
from django.urls import path
from aplicaciones.inicio.views import inicio, err_permisos
from aplicaciones.fuds.views import MotivoCreate, MotivoUpdate, MotivoList, MotivoDelete,\
ConformidadCreate,ConformidadUpdate,ConformidadList,ConformidadDelete,\
FudCreate, FudList, FudUpdate, FudDelete,\
TramiteCreate,TramiteUpdate,TramiteDelete,TramiteList

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

    path('NuevoTramite/', TramiteCreate.as_view(), name='NuevoTramite'),
    path('EditarTramite/<int:pk>/', TramiteUpdate.as_view(), name='EditarTramite'),
    path('ListarTramites/', TramiteList.as_view(), name='ListarTramites'),
    path('EliminarTramite/<int:pk>/', TramiteDelete.as_view(), name='EliminarTramite'),

    path('nuevo_fud/', FudCreate.as_view(), name='fud_create'),
    path('list/fud/', FudList.as_view(), name='fud_list'),
    path('update/fud/<int:pk>/', FudUpdate.as_view(), name='fud_update'),
    path('eliminar/fud/<int:pk>/', FudDelete.as_view(), name='fud_delete'),

    path('permisos/', err_permisos, name='need_permisos'),
]