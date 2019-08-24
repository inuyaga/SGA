from django.contrib import admin
from django.urls import path
from aplicaciones.pedidos import views as PedidoViews
from django.conf import settings
from django.conf.urls.static import static
app_name = "pedidos"
urlpatterns = [

    path('add/area/', PedidoViews.AreaCreate.as_view(), name='crear_area'),
    path('list/area/', PedidoViews.AreaList.as_view(), name='listar_area'),
    path('update/area/<int:pk>/', PedidoViews.AreaUpdate.as_view(), name='update_area'),
    path('delete/area/<int:pk>/', PedidoViews.AreaDelete.as_view(), name='eliminar_area'),

    path('update/marca/<int:pk>/', PedidoViews.MarcaUpdate.as_view(), name='update_marca'),
    path('delete/marca/<int:pk>/', PedidoViews.MarcaDelete.as_view(), name='eliminar_marca'), 
    path('list/marca/', PedidoViews.MarcaList.as_view(), name='listar_marca'),
    path('add/marca/', PedidoViews.MarcaCreate.as_view(), name='crear_marca'),  


    path('update/producto/<slug:pk>/', PedidoViews.ProductoUpdate.as_view(), name='update_producto'),
    path('update/producto_kit/<slug:pk>/', PedidoViews.ProductoKitUpdate.as_view(), name='update_producto_kit'),
    path('delete/producto/<slug:pk>/', PedidoViews.ProductoDelete.as_view(), name='eliminar_producto'),
    path('list/producto/', PedidoViews.ProductoList.as_view(), name='listar_producto'),
    path('add/producto/', PedidoViews.ProductoCreate.as_view(), name='crear_producto'),
    path('add/producto/kit/', PedidoViews.ProductokitCreate.as_view(), name='crear_producto_kit'),
 
    path('compra_sucursal/seleccion-tipo-de-compra', PedidoViews.SelectTipoCompraView.as_view(), name='pedido_select_compra'),  
    path('compra_sucursal/<int:pk>/', PedidoViews.ProductoCompraList.as_view(), name='pedido_tienda'), 
    path('compra_sucursal/pre_pedido', PedidoViews.DetalleList.as_view(), name='pedido_tienda_listado'), 
    path('compra_sucursal/pre_pedido/delete/<int:pk>/', PedidoViews.DetalleDelete.as_view(), name='detalle_producto_delete'),
    path('compra_sucursal/pre_pedido/confirm_pedido/add/<int:tipo>/', PedidoViews.Crear_pedido_tiendaView.as_view(), name='creacion_pedido_sucursal'),
    path('compra_sucursal/pedido/list/', PedidoViews.PedidoListSucursal.as_view(), name='pedido_sucursal_list'), 


    path('list/pedidos/', PedidoViews.PedidoList.as_view(), name='pedidos_list'),   
    path('list/pedidos/detalles/<int:pk>', PedidoViews.dowload_pedido_detalles.as_view(), name='pedidos_list_detalles'), 
    path('list/pedidos/update/<int:pk>/', PedidoViews.PedidoUpdate.as_view(), name='pedido_update'), 

    path('config/list/', PedidoViews.ConfigPedidoListView.as_view(), name='pedido_config'),
    path('config/crar/', PedidoViews.ConfigPedidoCreate.as_view(), name='pedido_config_crear'),
    path('config/crar/<int:pk>/', PedidoViews.ConfigPedidoUpdate.as_view(), name='pedido_config_update'),

    path('descargar/report/sucursales/', PedidoViews.dowload_report_pedidos.as_view(), name='down_report_suc'),
    path('descargar/report/detalles/pedidos/', PedidoViews.DowloadDetallesporPedido.as_view(), name='down_report_detalle_pedido'),
    path('config/pedido/list', PedidoViews.TipoPedidoList.as_view(), name='config_tipo_pedido_list'),
    path('config/pedido/crear', PedidoViews.TipoPedidoCrear.as_view(), name='config_tipo_pedido_crear'),
    path('config/pedido/update/<int:pk>/', PedidoViews.TipoPedidoEdit.as_view(), name='config_tipo_pedido_update'),
    path('config/pedido/delete/<int:pk>/', PedidoViews.TipoPedidoDelete.as_view(), name='config_tipo_pedido_delete'),
    path('asig/gastos/depos/', PedidoViews.AsigGastoList.as_view(), name='asig_gasto_list'), 
    path('asig/gastos/depos/crear', PedidoViews.AsigGastoCrear.as_view(), name='asig_gasto_create'), 
    path('asig/gastos/depos/update/<int:pk>/', PedidoViews.AsigGastoUpdate.as_view(), name='asig_gasto_update'), 
    path('asig/gastos/depos/delete/<int:pk>/', PedidoViews.AsigGastoDelete.as_view(), name='asig_gasto_delete'), 


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)