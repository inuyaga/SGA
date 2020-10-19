from django.contrib import admin
from django.urls import path 
from aplicaciones.web import views as web_dash
app_name="web"
urlpatterns = [
    path('', web_dash.Home.as_view(), name='inicio'),
    path('list/producto/', web_dash.ProductosListWebView.as_view(), name='list_prod'), 
    # path('producto/detalle/<slug:pk>/<slug:nombre>', web_dash.ProductoDetalleView.as_view(), name='producto_detalle'),
    path('events/inscribir/', web_dash.IncribirCreate.as_view(), name='inscripcion'),
    path('vancante/list/', web_dash.VacanteView.as_view(), name='vacantes'),
    path('vancante/postulacion/', web_dash.PostularCreate.as_view(), name='va_postular'),
    path('registro/user/computel/', web_dash.CreateUser.as_view(), name='registro'),
    path('registro/busqueda/rfc/', web_dash.FindRfcUserView, name='rfc_find'),
    path('add/producto/carrito/compra', web_dash.AddProductoCarrito, name='add_producto'),
    path('get/productos/carrito/compra', web_dash.get_carro_compras, name='get_count_prod'),
    path('carrito/compra/view/', web_dash.CarritoComprasView.as_view(), name='carrito'),
    path('carrito/compra/delete', web_dash.delete_item_carrito, name='delete_item'),
    path('carrito/compra/checkout', web_dash.CheckoutView.as_view(), name='checkout'),

    path('domicilios/listar/', web_dash.DomicilioListView.as_view(), name='dom_list'),
    path('domicilios/create/', web_dash.DomicilioCreateView.as_view(), name='dom_crear'),
    path('domicilios/<int:pk>/update/', web_dash.DomicilioUpdateView.as_view(), name='dom_update'),

    path('compras/pedidos/', web_dash.ComprasWebList.as_view(), name='compras_web'),
    path('compras/pedidos/<int:pk>/detalles/', web_dash.DetalleCmpraWebView.as_view(), name='compras_web_detalle'),
    path('cuenta/user/', web_dash.DetalleCuentaView.as_view(), name='profile'),
    path('blog/view/<int:pk>/<slug:nombre>/', web_dash.BlogViewSingle.as_view(), name='blog_view'),
    
    
    # Direcciones de la versión fea lic leo
    path('nuestraempresa', web_dash.NuestraEmpresa.as_view(), name='nuestraempresav2'),
    path('politicas', web_dash.PoliticasDevoluciones.as_view(), name='politicasdevov2'),
    path('serviciocliente', web_dash.ServicioCliente.as_view(), name='servicioclientev2'),
    path('contacto', web_dash.Contacto.as_view(), name='contactov2'),
    path('producto/detalle/<slug:pk>/<slug:nombre>', web_dash.ProductoDetalleViewV2.as_view(), name='producto_detalle_v'),
]