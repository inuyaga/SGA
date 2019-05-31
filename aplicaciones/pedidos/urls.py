from django.contrib import admin
from django.urls import path
from aplicaciones.pedidos.views import AreaCreate, AreaList, AreaUpdate, AreaDelete, MarcaCreate, MarcaList, \
MarcaUpdate, MarcaDelete, ProductoCreate, ProductoList, ProductoDelete, ProductoUpdate, ProductoCompraList, \
DetalleList, DetalleDelete, PedidoList, PedidoUpdate, PedidoListSucursal, ProductokitCreate, \
ProductoKitUpdate, dowload_pedido_detalles, SelectTipoCompraView, Crear_pedido_tiendaView, ConfigPedidoListView, \
ConfigPedidoCreate, ConfigPedidoUpdate
from django.conf import settings
from django.conf.urls.static import static
app_name = "pedidos"
urlpatterns = [

    path('add/area/', AreaCreate.as_view(), name='crear_area'),
    path('list/area/', AreaList.as_view(), name='listar_area'),
    path('update/area/<int:pk>/', AreaUpdate.as_view(), name='update_area'),
    path('delete/area/<int:pk>/', AreaDelete.as_view(), name='eliminar_area'),

    path('update/marca/<int:pk>/', MarcaUpdate.as_view(), name='update_marca'),
    path('delete/marca/<int:pk>/', MarcaDelete.as_view(), name='eliminar_marca'), 
    path('list/marca/', MarcaList.as_view(), name='listar_marca'),
    path('add/marca/', MarcaCreate.as_view(), name='crear_marca'),  


    path('update/producto/<slug:pk>/', ProductoUpdate.as_view(), name='update_producto'),
    path('update/producto_kit/<slug:pk>/', ProductoKitUpdate.as_view(), name='update_producto_kit'),
    path('delete/producto/<slug:pk>/', ProductoDelete.as_view(), name='eliminar_producto'),
    path('list/producto/', ProductoList.as_view(), name='listar_producto'),
    path('add/producto/', ProductoCreate.as_view(), name='crear_producto'),
    path('add/producto/kit/', ProductokitCreate.as_view(), name='crear_producto_kit'),

    path('compra_sucursal/seleccion-tipo-de-compra', SelectTipoCompraView.as_view(), name='pedido_select_compra'), 
    path('compra_sucursal/<int:tipo>/', ProductoCompraList.as_view(), name='pedido_tienda'),
    path('compra_sucursal/pre_pedido', DetalleList.as_view(), name='pedido_tienda_listado'), 
    path('compra_sucursal/pre_pedido/delete/<int:pk>/', DetalleDelete.as_view(), name='detalle_producto_delete'),
    path('compra_sucursal/pre_pedido/confirm_pedido/add/<int:tipo>/', Crear_pedido_tiendaView.as_view(), name='creacion_pedido_sucursal'),
    path('compra_sucursal/pedido/list/', PedidoListSucursal.as_view(), name='pedido_sucursal_list'),


    path('list/pedidos/', PedidoList.as_view(), name='pedidos_list'), 
    path('list/pedidos/detalles/<int:pk>', dowload_pedido_detalles.as_view(), name='pedidos_list_detalles'), 
    path('list/pedidos/update/<int:pk>/', PedidoUpdate.as_view(), name='pedido_update'),

    path('config/list/', ConfigPedidoListView.as_view(), name='pedido_config'),
    path('config/crar/', ConfigPedidoCreate.as_view(), name='pedido_config_crear'),
    path('config/crar/<int:pk>/', ConfigPedidoUpdate.as_view(), name='pedido_config_update'),


    



]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)