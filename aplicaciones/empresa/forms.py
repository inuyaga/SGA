from django import forms
from aplicaciones.empresa.models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = (
            'cli_nombre',
            'cli_calle',
            'cli_colonia',
            'cli_cp',
            'cli_estado',
            'cli_telefono',
            'cli_email',
            'cli_vndedor_asignado',
            'cli_status',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
