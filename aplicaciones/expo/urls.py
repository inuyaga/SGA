
from django.urls import path
from aplicaciones.expo import views as ExpoView

app_name = "expo"
urlpatterns = [
    path('select/cliente/', ExpoView.SelectCienteView.as_view(), name='selec_cliente'),
    path('select/cliente/venta/', ExpoView.VentaView.as_view(), name='venta'), 
    path('ventas/list/', ExpoView.VentaList.as_view(), name='venta_list'), 
    path('ventas/list/detalle', ExpoView.DetalleVentaList.as_view(), name='detalle_vent'), 
    ]