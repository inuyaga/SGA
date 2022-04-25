from django.contrib import admin
from django.urls import path, re_path
from aplicaciones.pago_proveedor.views import ProveedorList, ProveedorCreate, ProveedorUpdate, \
ProveedorDelete, ContratosList, ContratoCreate, ContratoDelete, ContratoUpdate,  \
ContratoDetalle, PagoCreate, PagoCreateP, PagoList, PagoUpdateOb, PagoDelete, PagoUpdate,  \
report_contratso, CasaDeptoList, CasaDeptoAdd
# from aplicaciones.inicio.views import inicio
app_name = "proveedor"
urlpatterns = [
    # URLS DE PROVEEDORES
    path('excel/', report_contratso.as_view(), name='nuevo_excel'),
    path('nuevo/', ProveedorCreate.as_view(), name='nuevo'),
    path('lista/', ProveedorList.as_view(), name='lista'),
    re_path(r'^editar/(?P<pk>\d+)/$', ProveedorUpdate.as_view(), name='edicion_p'),
    re_path(r'^eliminar/(?P<pk>\d+)/$', ProveedorDelete.as_view(), name='eliminar'),
    
    # URLS DE CONTRATOS
    path('contrato/detalle/<int:pk>', ContratoDetalle.as_view(), name='contrato_detalle'),
    path('contrato/listar/', ContratosList.as_view(), name='contrato_listar'),
    path('contrato/nuevo/', ContratoCreate.as_view(), name='contrato_nuevo'),
    re_path(r'^contrato/eliminar/(?P<pk>\d+)/$', ContratoDelete.as_view(), name='contrato_eliminar'),
    re_path(r'^contrato/editar/(?P<pk>\d+)/$', ContratoUpdate.as_view(), name='contrato_edicion'),
   
    # URLS DE PAGOS
    path('pago/crear/<int:pk>/', PagoCreateP.as_view(), name='pago_crear'),
    path('pago/generar/<int:pk>/', PagoCreate.as_view(), name='pago_generar'),
    # path('pago/listar/', PagoList.as_view(), name='pago_listar'),
    path('pago/eliminar/<int:pk>/<int:id_pago>/', PagoDelete.as_view(), name='pago_eliminar'),
    path('pago/editar/<int:pk>/', PagoUpdate.as_view(), name='pago_edicion'),
    path('pago/nota/<int:pk>/', PagoUpdateOb.as_view(), name='pago_observacion'),
    # path('pago/complemento/<int:pk>/', ComplementoCreate.as_view(), name='complemento_crear'),
    # path('pago/complemento/eliminar/<int:pk>/<int:id_comp>/', ComplementoDelete.as_view(), name='complemento_delete'), 

    path('locacion/lista/', CasaDeptoList.as_view(), name='depto_casa_lista'),
    path('agregar/locacion', CasaDeptoAdd.as_view(), name='depto_casa_add'),
   

]
 