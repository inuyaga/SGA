from django.urls import path, include, re_path
from aplicaciones.empresa import views as EmpresaView
app_name="empresa" 
urlpatterns = [
    path('cliente/list/', EmpresaView.ClienteList.as_view(), name="clientes_list"),
    path('cliente/update/<int:pk>/', EmpresaView.ClienteUpdate.as_view(), name="clientes_update"),
]