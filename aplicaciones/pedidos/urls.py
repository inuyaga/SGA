from django.contrib import admin
from django.urls import path
from aplicaciones.pedidos.views import AreaCreate, AreaList, AreaUpdate, AreaDelete, MarcaCreate, MarcaList, \
MarcaUpdate, MarcaDelete, ProductoCreate, ProductoList, ProductoDelete, ProductoUpdate, ProductoCompraList, \
DetalleList, DetalleDelete, Crear_pedido_tienda, PedidoList, PedidoUpdate, PedidoListSucursal
# from aplicaciones.inicio.views import inicio
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
    path('delete/producto/<slug:pk>/', ProductoDelete.as_view(), name='eliminar_producto'),
    path('list/producto/', ProductoList.as_view(), name='listar_producto'),
    path('add/producto/', ProductoCreate.as_view(), name='crear_producto'),

    path('compra_sucursal/', ProductoCompraList.as_view(), name='pedido_tienda'),
    path('compra_sucursal/pre_pedido', DetalleList.as_view(), name='pedido_tienda_listado'),
    path('compra_sucursal/pre_pedido/delete/<int:pk>/', DetalleDelete.as_view(), name='detalle_producto_delete'),
    path('compra_sucursal/pre_pedido/confirm_pedido/add/', Crear_pedido_tienda, name='creacion_pedido_sucursal'),
    path('compra_sucursal/pedido/list', PedidoListSucursal.as_view(), name='pedido_sucursal_list'),


    path('list/pedidos/', PedidoList.as_view(), name='pedidos_list'),
    path('list/pedidos/update/<int:pk>/', PedidoUpdate.as_view(), name='pedido_update'),



]