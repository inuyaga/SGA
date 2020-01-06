from django import forms
from aplicaciones.pedidos.models import (Area, Marca, Producto, Pedido, Configuracion_pedido, Tipo_Pedido, Asignar_gasto_sucursal, Catalogo_Productos,
Inventario)


from django.contrib.auth import get_user_model
Usuario = get_user_model()
from ajax_select.fields import AutoCompleteSelectMultipleField
class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ('area_nombre',)

    def __init__(self, *args, **kwargs):
        super(AreaForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MarcaForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ProductoForm(forms.ModelForm): 
    class Meta:
        model = Producto
        # fields = '__all__'
        exclude = ['producto_productos', 'producto_kit']

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['producto_es_kit'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['producto_visible'].widget.attrs.update({'class': 'form-check-input'})

class ProductoKitForm(forms.ModelForm):
    class Meta:
        model = Producto
        # fields = '__all__'
        exclude = ['producto_kit', 'producto_es_kit']
    
    producto_productos = AutoCompleteSelectMultipleField('productos_tags_kits',required=False, help_text='Codigo producto')

    def __init__(self, *args, **kwargs):
        super(ProductoKitForm, self).__init__(*args, **kwargs)
        self.fields['producto_productos'].queryset = Producto.objects.filter(producto_es_kit=True)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields['producto_visible'].widget.attrs.update({'class': 'form-check-input'})

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ('pedido_id_depo','pedido_status', 'pedido_n_factura', 'pedido_n_cresscedo')

    def __init__(self, *args, **kwargs):
        super(PedidoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class PedidoVentaForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ('pedido_n_cresscedo', )

    def __init__(self, *args, **kwargs):
        super(PedidoVentaForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class PedidoFacturaForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ('pedido_n_factura', )

    def __init__(self, *args, **kwargs):
        super(PedidoFacturaForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
class PedidoSalidaForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ('pedido_n_salida', )

    def __init__(self, *args, **kwargs):
        super(PedidoSalidaForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ConfigForm(forms.ModelForm):
    class Meta:
        model = Configuracion_pedido
        fields = '__all__'
        widgets = {
        'conf_fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
        'conf_fecha_fin' : forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(ConfigForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class Tipo_PedidoForm(forms.ModelForm):
    class Meta:
        model = Tipo_Pedido
        fields = '__all__'

    tp_productos = AutoCompleteSelectMultipleField('productos_tags',required=False, help_text='Codigo producto')
    def __init__(self, *args, **kwargs):
        super(Tipo_PedidoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
class AsigGastoForm(forms.ModelForm):
    class Meta:
        model = Asignar_gasto_sucursal
        fields = '__all__'

    # tp_productos = AutoCompleteSelectMultipleField('productos_tags',required=False, help_text='Codigo producto')
    def __init__(self, *args, **kwargs):
        super(AsigGastoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class Catalogo_ProductosForm(forms.ModelForm):
    class Meta:
        model = Catalogo_Productos
        fields = ['tp_empresa','tp_catalogo','tp_descripcion','tp_no_licitacion','tp_imagen','tp_orientacion_t', 'tp_productos']
    tp_productos = AutoCompleteSelectMultipleField('productos_tags_catalogo',required=False, help_text='Codigo producto')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class InventarioResguardoForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['inv_conteo','inv_cant_resguardo']
    inv_producto = forms.CharField(label='Codigo producto', max_length=100)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class InventarioPikinForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['inv_conteo','inv_cant_piking']
    inv_producto = forms.CharField(label='Codigo producto', max_length=100)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class InventarioOtrosForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['inv_conteo','inv_cant_otros', 'inv_descripcion']
    inv_producto = forms.CharField(label='Codigo producto', max_length=100)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class InventarioMermaForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['inv_conteo','inv_cant_merma', 'inv_descripcion', 'inv_sup_autorizo_merma']
    inv_producto = forms.CharField(label='Codigo producto', max_length=100)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['inv_sup_autorizo_merma'].queryset=Usuario.objects.filter(is_staff=True)

class InventarioEdit(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['inv_conteo','inv_cant_resguardo', 'inv_cant_piking', 'inv_cant_otros', 'inv_cant_merma']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
