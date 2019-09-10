from aplicaciones.activos import views as Vactivos
from django.urls import path
app_name = "activos"
urlpatterns = [
    # path('', Vactivos.Prueba.as_view(), name='index'),
    path('categoria/create/', Vactivos.CategoriaCrear.as_view(), name='create_categorias'),
    path('categoria/update/<int:pk>/', Vactivos.CategoriaUpdate.as_view(), name='cat_update'),
    path('categoria/listar/', Vactivos.CategoriaList.as_view(), name='cat_list'),
    path('categoria/delete/<int:pk>/', Vactivos.CategoriaDelete.as_view(), name='cat_delete'),

    path('activo/listar/', Vactivos.ActivoList.as_view(), name='activo_list'),
    path('activo/crear/', Vactivos.ActivoCrear.as_view(), name='activo_crear'),
    path('activo/update/<int:pk>/', Vactivos.ActivoUpdate.as_view(), name='activo_update'),
    path('activo/delete/<int:pk>/', Vactivos.ActivoDelete.as_view(), name='activo_delete'),

    path('activo/especificacion/agreagar/<int:pk>/', Vactivos.EspecificacioCreate.as_view(), name='activo_especificacion_crear'),
    path('activo/especific/<int:activo>/<int:pk>/', Vactivos.EspUpdate.as_view(), name='activo_esp_update'),
    path('activo/especific/delete/<int:activo>/<int:pk>/', Vactivos.EspDelete.as_view(), name='activo_esp_delete'),

    path('activo/asignacion/user/list/', Vactivos.AsignacionList.as_view(), name='activo_asignar_list'),
    path('activo/asignacion/user/crear/', Vactivos.AsignacionCrear.as_view(), name='activo_asignar'),
    path('activo/asignacion/user/pdf/', Vactivos.GeneraPdfAsignacion.as_view(), name='activo_asignar_pdf'),
]