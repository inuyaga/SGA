from __future__ import absolute_import
from django.conf.urls import url, include
from appis.inicio.views import inicio
app_name = "inicio"
urlpatterns = [
    url(r'^$', inicio, name='index'), 
]
