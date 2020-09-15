from django.contrib import admin
from django.urls import path 
from aplicaciones.api_mobile import views as api
app_name="api_mobile"
urlpatterns = [
    path('get/cliente/<slug:cliente>', api.GetClienteInfo.as_view(), name='cliente'),
    path('visitas/vendedors/api/', api.VisitaVendedorView.as_view(), name='createvisita'),
]