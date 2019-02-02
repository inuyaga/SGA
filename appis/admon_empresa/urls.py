from __future__ import absolute_import
from django.conf.urls import url, include
from appis.admon_empresa.views
app_name = "admon"
urlpatterns = [
    url(r'^$', compra_tienda, name='index'),
    # url(r'^buscar/', busquedafiltro, name='buscar'),
    #url(r'^buscar/', busquedafiltro, name='buscar'),
]
