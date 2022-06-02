from django.contrib import admin
from django.urls import path
from aplicaciones.solicitud import views as SolicitudView

app_name = "solicitud"
urlpatterns = [
    path('tipo_de_servicio/', SolicitudView.TipoServicioCreate.as_view(), name='crear_tipo_servicio'),
    path('tipo_de_servicio/<int:pk>/editar', SolicitudView.TipoServicioEdit.as_view(), name='tipservicio_edit'),
    path('tipo_de_servicio/<int:pk>/eliminar', SolicitudView.TipoServicioDelete.as_view(), name='tipservicio_delete'),
    path('servicio/', SolicitudView.ServicioList.as_view(), name='servicios'),
    path('servicio/crear/', SolicitudView.ServicioCreate.as_view(), name='servicio_crear'),
    path('servicio/validar/<slug:pk>/', SolicitudView.ServicioValidarView.as_view(), name='servicio_validar'),
    path('servicio/cierre/<slug:pk>/', SolicitudView.ServicioCerrarView.as_view(), name='servicio_cerrar'),
    path('servicio/eliminar/<slug:pk>/', SolicitudView.ServicioDelete.as_view(), name='servicio_delete'),
    path('servicio/autoriza/', SolicitudView.UpdateStatusServicioView.as_view(), name='servicio_autoriza'),

    path('activo/listar/download/report/', SolicitudView.Download_report_servicio.as_view(), name='dwload_report_solicitudes'),
]