from django import forms
from aplicaciones.expo.models import VentaExpo
from ajax_select.fields import AutoCompleteSelectField
from aplicaciones.pedidos.models import Producto
class VentaExpoForm(forms.ModelForm): 
    class Meta:
        model = VentaExpo 
        fields = '__all__' 
    
    venta_e_cliente = AutoCompleteSelectField('ClientesVentasExpo',required=True, help_text='Codigo Cliente')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class EditProductoExpoForm(forms.ModelForm): 
    class Meta:
        model = Producto 
        fields = {'producto_nombre', 'producto_descripcion', 'producto_imagen', 'prducto_codigo_barras'}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})