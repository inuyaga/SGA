from django.contrib import admin
from django.urls import path 
from aplicaciones.web import views as web_dash
app_name="web"
urlpatterns = [
    path('', web_dash.Home.as_view(), name='inicio'),
    path('list/producto/prospecto/', web_dash.ProductosListWebView.as_view(), name='list_prod'), 
    path('producto/detalle/<slug:pk>/', web_dash.ProductoDetalleView.as_view(), name='producto_detalle'),
    path('events/inscribir/', web_dash.IncribirCreate.as_view(), name='inscripcion'),
    path('vancante/list/', web_dash.VacanteView.as_view(), name='vacantes'),
    path('vancante/postulacion/', web_dash.PostularCreate.as_view(), name='va_postular'),
    path('registro/user/computel/', web_dash.CreateUser.as_view(), name='registro'),
    path('registro/busqueda/rfc/', web_dash.FindRfcUserView, name='rfc_find'),
    path('add/producto/carrito/compra', web_dash.AddProductoCarrito, name='add_producto'),
    path('get/productos/carrito/compra', web_dash.get_carro_compras, name='get_count_prod'),
    path('carrito/compra', web_dash.CarritoComprasView.as_view(), name='carrito'),
    path('carrito/compra/delete', web_dash.delete_item_carrito, name='delete_item'),
    path('carrito/compra/1', web_dash.CompraStep1View.as_view(), name='step1'),
    path('domicilios/listar/', web_dash.DomicilioListView.as_view(), name='dom_list'),
    path('domicilios/create/', web_dash.DomicilioCreateView.as_view(), name='dom_crear'),
    path('domicilios/<int:pk>/update/', web_dash.DomicilioUpdateView.as_view(), name='dom_update'),
    path('compras/cliente/', web_dash.ComprasWebList.as_view(), name='compras_web'),
    path('compras/cliente/<int:pk>/detalles/', web_dash.DetalleCmpraWebView.as_view(), name='compras_web_detalle'),
    path('cuenta/user/', web_dash.DetalleCuentaView.as_view(), name='profile'),
]