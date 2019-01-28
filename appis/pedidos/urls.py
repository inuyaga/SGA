from __future__ import absolute_import
from django.conf.urls import url, include
from appis.pedidos.views import compra_tienda, busquedafiltro
app_name = "pedidos"
urlpatterns = [
    url(r'^$', compra_tienda, name='index'),
    url(r'^buscar/', busquedafiltro, name='buscar'),
    #url(r'^buscar/', busquedafiltro, name='buscar'),
]
