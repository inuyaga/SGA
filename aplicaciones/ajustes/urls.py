
from django.urls import path
from aplicaciones.ajustes import views as ViewsAjust

app_name = "ajustes"
urlpatterns = [
    path('listar/', ViewsAjust.AjusteListView.as_view(), name='listar'),
    path('añadir/', ViewsAjust.AjusteCrearView.as_view(), name='add'),
    path('busqueda/producto/', ViewsAjust.ProductoGetCodigo.as_view(), name='buscar'),
    path('ajuste/<int:pk>/eliminar/', ViewsAjust.AjusteDelete.as_view(), name='eliminar_ajuste'),
    path('ajuste/<int:pk>/cambiar/', ViewsAjust.AjusteUpdateCresendoView.as_view(), name='updater_ajuste'),
    path('ajuste/<int:pk>/update/', ViewsAjust.AjusteUpdateView.as_view(), name='ajuste_actualizar'),
]