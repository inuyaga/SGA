from django.urls import path
from aplicaciones.ods import views as ods_view

app_name = "orden_serv"
urlpatterns = [
    path('list/', ods_view.OrdenServiciotListView.as_view(), name='list_ods'),
    path('crear/', ods_view.OrdenServicioCreateView.as_view(), name='ods_create'), 
    path('tecnico/darseguimiento/<int:pk>/', ods_view.OrdenServicioSeguirCreate.as_view(), name='ods_create'), 
    path('tecnico/ods/update/<int:pk>/', ods_view.OrdenServicioEditTecnico.as_view(), name='ods_tecnico_update'), 
    path('tecnico/ods/genera/format/pdf/<int:pk>/', ods_view.OdsGeneraPDF.as_view(), name='ods_pdf'), 
    path('tecnico/ods/soporte/terminar/<int:pk>/', ods_view.OrdenServicioTerminarSoporteCreate.as_view(), name='ods_terminar'), 
    path('delete/confirmar/<int:pk>/', ods_view.OrdenServicioDelete.as_view(), name='ods_delete'), 
    path('user/confirmar/procesos/<int:pk>/', ods_view.OdsValidarPorUser.as_view(), name='ods_cerrar'), 
    path('refaccion/list/<int:pk>/', ods_view.RefaccionOdsList.as_view(), name='ods_refaccion'), 

    path('refaccion/add/<int:ID_ods>/', ods_view.RefaccionCrear.as_view(), name='ods_crear_refaccion'), 
    path('refaccion/delete/<int:pk>/<int:ID_ods>/', ods_view.RefaccionDelete.as_view(), name='ods_delete_refaccion'), 
]