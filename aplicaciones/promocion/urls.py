from django.contrib import admin
from django.urls import path 
from aplicaciones.promocion import views as VistasPromo

app_name="promocion"
urlpatterns = [
    path('update/masive/', VistasPromo.ProductosInsertPromo.as_view(), name='update_masive_promo'),
    path('puntos/', VistasPromo.PromoList.as_view(), name='promopuntolistaG'),
    path('detalle/puntos/<slug:nombre>/', VistasPromo.PromoListDetalle.as_view(), name='promopuntolistaD'),
]