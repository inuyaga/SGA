from django.contrib import admin
from django.urls import path
from aplicaciones.inicio.views import inicio, err_permisos
from aplicaciones.fuds.views import MotivoCreate, MotivoUpdate, MotivoList, MotivoDelete, FudCreate, FudList
app_name = "fuds"
urlpatterns = [
    path('NuevoMotivo/', MotivoCreate.as_view(), name='NuevoMotivo'),
    path('EditarMotivo/<int:pk>/', MotivoUpdate.as_view(), name='EditarMotivo'),
    path('ListarMotivo/', MotivoList.as_view(), name='ListarMotivo'),
    path('EliminarMotivo/<int:pk>/', MotivoDelete.as_view(), name='EliminarMotivo'),
    path('permisos/', err_permisos, name='need_permisos'),

    path('nuevo_fud/', FudCreate.as_view(), name='fud_create'),
    path('list/fud/', FudList.as_view(), name='fud_list'),
    path('update/fud/', FudList.as_view(), name='fud_update'),
    path('delete/fud/', FudList.as_view(), name='fud_delete'),
]