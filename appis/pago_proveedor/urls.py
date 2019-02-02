from __future__ import absolute_import
from django.conf.urls import url, include
from appis.pago_proveedor.views import ProveedorList, ProveedorCreate, ProveedorUpdate, ProveedorDelete, ContratosList, ContratoCreate
app_name = "proveedor"
urlpatterns = [
    # url(r'^$', nuevo_proveedor, name='index'),
    url(r'^nuevo', ProveedorCreate.as_view(), name='nuevo'),
    url(r'^lista', ProveedorList.as_view(), name='lista'),
    url(r'^editar/(?P<pk>\d+)/', ProveedorUpdate.as_view(), name='edicion_p'),
    url(r'^eliminar/(?P<pk>\d+)/', ProveedorDelete.as_view(), name='eliminar'),
    url(r'^contrato/listar/', ContratosList.as_view(), name='contrato_listar'),
    url(r'^contrato/nuevo/', ContratoCreate.as_view(), name='contrato_nuevo'),

    # url(r'^buscar/', busquedafiltro, name='buscar'),
    #url(r'^buscar/', busquedafiltro, name='buscar'),
]
