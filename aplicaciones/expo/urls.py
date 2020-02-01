
from django.urls import path
from aplicaciones.expo import views as ExpoView

app_name = "expo"
urlpatterns = [
    path('select/cliente/', ExpoView.SelectCienteView.as_view(), name='selec_cliente'),
    path('select/cliente/venta/', ExpoView.VentaView.as_view(), name='venta'), 
    path('ventas/list/', ExpoView.VentaList.as_view(), name='venta_list'), 
    path('ventas/list/detalle', ExpoView.DetalleVentaList.as_view(), name='detalle_vent'), 
    path('ventas/list/delete/<int:pk>/', ExpoView.VentaDelete.as_view(), name='delete_venta'), 
    path('ventas/list/update/<int:pk>/', ExpoView.VentaExpoUpdate.as_view(), name='update_venta'), 
    path('ventas/list/detalle/venta/delete/<int:pk>/', ExpoView.DetalleVentaDelete.as_view(), name='delete_detalle_venta'), 
    ]