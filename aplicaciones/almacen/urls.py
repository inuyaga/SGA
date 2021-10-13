
from django.urls import path
from aplicaciones.almacen import views as almacen_views

app_name = "almacen"
urlpatterns = [
    path('crear/', almacen_views.CreatePedido.as_view(), name='crear')
]