from django.contrib import admin
from django.urls import path
from aplicaciones.inicio.views import err_permisos
from aplicaciones.descargas.views import DescargasList, DescargaCreate, DescargaUpdate, DescargaDelete

app_name = "descargas"
urlpatterns = [
    path('descargasList/', DescargasList.as_view(), name='listadescargas'),
    path('creardescarga/', DescargaCreate.as_view(), name='creardescarga'),
    path('actualizardescarga/<int:pk>/', DescargaUpdate.as_view(), name='actualizardescarga'),
    path('eliminardescarga/<int:pk>/', DescargaDelete.as_view(), name='eliminardescarga'),

]