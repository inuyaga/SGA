
from django.urls import path
from aplicaciones.gasto import views as GastoView

app_name = "gastos"
urlpatterns = [
    path('inicio', GastoView.InicioView.as_view(), name='init'),
    path('tipo_gasto/crear/', GastoView.CrearTipoGasto.as_view(), name='tipo_crear'),
    path('tipo_gasto/list/', GastoView.TipoGastoList.as_view(), name='tipoGastoList'),
    path('tipo_gasto/<int:pk>/update/', GastoView.UpdateTipoGasto.as_view(), name='updateTipoG'),
    path('tipo_gasto/<int:pk>/delete/', GastoView.TipoGastoDelete.as_view(), name='deleteTipoG'),
    path('gasto/list/', GastoView.GastoViewList.as_view(), name='gasto_list'),
    path('gasto/<int:pk>-detalle/', GastoView.GastoDetalleView.as_view(), name='gasto_detalle'),
    path('gasto/crear/', GastoView.GastoCreate.as_view(), name='gasto_create'),
    path('gasto/<int:pk>/update/', GastoView.GastoUpdateView.as_view(), name='gasto_update'),
    path('gasto/renta/', GastoView.GastoRentaViewList.as_view(), name='gastorenta_list'),
    path('update/status/', GastoView.UpdateStatusView.as_view(), name='gasto_update_status'),
    path('update/status/renta/', GastoView.UpdateStatusRentaView.as_view(), name='gasto_updaterenta_status'),
    path('<int:pk>/delete/', GastoView.GastoDelete.as_view(), name='gasto_delete'),
    path('reembolso/list/', GastoView.ReembolsoList.as_view(), name='reembolso_list'),
    path('reembolso/list/rentas/', GastoView.ReembolsoRentaList.as_view(), name='reembolsoRenta_list'),
    path('reembolso/dowload/', GastoView.Download_report_reembolso.as_view(), name='reembolso_dowload'),
    path('reembolso/dowload/renta/', GastoView.Download_report_reembolsoRenta.as_view(), name='reembolsoRenta_download'),
    path('gasto/dowload/', GastoView.Download_Gasto.as_view(), name='gasto_dowload'),
    ]