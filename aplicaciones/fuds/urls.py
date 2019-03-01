from django.contrib import admin
from django.urls import path
from aplicaciones.inicio.views import inicio, err_permisos
from aplicaciones.fuds.views import MotivoCreate, MotivoUpdate, MotivoList, MotivoDelete,ConformidadCreate,ConformidadUpdate,ConformidadList,ConformidadDelete
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
    path('permisos/', err_permisos, name='need_permisos'),
]