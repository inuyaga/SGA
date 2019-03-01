from django.contrib import admin
from django.urls import path
from aplicaciones.inicio.views import inicio, err_permisos
from aplicaciones.fuds.views import MotivoCreate, MotivoUpdate, MotivoList, MotivoDelete
app_name = "fuds"
urlpatterns = [
    path('NuevoMotivo/', MotivoCreate.as_view(), name='NuevoMotivo'),
    path('EditarMotivo/<int:pk>/', MotivoUpdate.as_view(), name='EditarMotivo'),
    path('ListarMotivo/', MotivoList.as_view(), name='ListarMotivo'),
    path('EliminarMotivo/<int:pk>/', MotivoDelete.as_view(), name='EliminarMotivo'),
    path('permisos/', err_permisos, name='need_permisos'),
]