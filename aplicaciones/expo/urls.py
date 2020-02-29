
from django.urls import path
from aplicaciones.expo import views as ExpoView

app_name = "expo"
urlpatterns = [
    path('select/cliente/', ExpoView.SelectCienteView.as_view(), name='selec_cliente'),
    path('select/cliente/venta/', ExpoView.VentaView.as_view(), name='venta'), 
    path('ventas/list/', ExpoView.VentaList.as_view(), name='venta_list'), 
    path('ventas/list/detalle/<int:pk>/', ExpoView.DetalleVentaList.as_view(), name='detalle_vent'), 
    path('ventas/list/delete/<int:pk>/', ExpoView.VentaDelete.as_view(), name='delete_venta'), 
    path('ventas/list/update/<int:pk>/', ExpoView.VentaExpoUpdate.as_view(), name='update_venta'), 
    path('ventas/list/detalle/venta/delete/<int:pk>/', ExpoView.DetalleVentaDelete.as_view(), name='delete_detalle_venta'), 
    path('producto/list/', ExpoView.ProductoListProveedor.as_view(), name='producto_list_proveedor'), 
    path('producto/update/producto/<slug:pk>/', ExpoView.ProductoExpoEdit.as_view(), name='update_producto_expo'), 
    path('ventas/expo/download/', ExpoView.dowload_ventas_expo.as_view(), name='download_expo_vent'), 
    path('ventas/expo/download/pedido/', ExpoView.dowload_venta_expo_ID.as_view(), name='download_expo_ventID'), 
    path('ventas/expo/download/pdf/recibo/cliente/', ExpoView.Pdf_recibo_cliente.as_view(), name='download_recibo_cliente'), 
    path('ventas/expo/download/xls/marcas/date/', ExpoView.TotalVentasMarcasDate.as_view(), name='download_total_ventas_date_marcas'), 
    ]