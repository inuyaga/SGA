from django.urls import path
from aplicaciones.ods import views as ods_view

app_name = "ods"
urlpatterns = [
    path('list/', ods_view.prueba.as_view(), name='list_ods')
]