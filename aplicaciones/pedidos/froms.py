from django import forms
from aplicaciones.pedidos.models import Area, Marca, Producto, Pedido
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

class ProductoKitForm(forms.ModelForm):
    class Meta:
        model = Producto
        # fields = '__all__'
        exclude = ['producto_kit', 'producto_es_kit']

    def __init__(self, *args, **kwargs):
        super(ProductoKitForm, self).__init__(*args, **kwargs)
        self.fields['producto_productos'].queryset = Producto.objects.filter(producto_es_kit=True)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ('pedido_id_depo','pedido_status')

    def __init__(self, *args, **kwargs):
        super(PedidoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})