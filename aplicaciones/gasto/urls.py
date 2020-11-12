
from django.urls import path
from aplicaciones.gasto import views as GastoView

app_name = "gastos"
urlpatterns = [
    path('inicio', GastoView.InicioView.as_view(), name='init'),
    path('tipo_gasto/crear/', GastoView.CrearTipoGasto.as_view(), name='tipo_crear'),
    ]