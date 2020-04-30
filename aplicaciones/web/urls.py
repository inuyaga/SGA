from django.contrib import admin
from django.urls import path
from aplicaciones.web import views as web_dash
app_name="web"
urlpatterns = [
    path('', web_dash.Home.as_view(), name='inicio'),
    path('events/inscribir/', web_dash.IncribirCreate.as_view(), name='inscripcion'),
    path('vancante/list/', web_dash.VacanteView.as_view(), name='vacantes'),
    path('vancante/postulacion/', web_dash.PostularCreate.as_view(), name='va_postular'),
]