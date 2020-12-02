from django.contrib import admin
from django.urls import path
from aplicaciones.inicio.views import err_permisos
from aplicaciones.compra.views import CompraList, CompraCreate, CompraUpdate

app_name = "compra"
urlpatterns = [
    path('listacompras/', CompraList.as_view(), name='listacompras'),
    path('crearcompra/', CompraCreate.as_view(), name='crearcompra'),
    path('actualizarcompra/<int:pk>/', CompraUpdate.as_view(), name='actualizarcompra'),

]