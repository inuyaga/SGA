from rest_framework import serializers
from aplicaciones.plan_de_trabajo.models import VisitaVendedor

class VisitaVendedorSerializer(serializers.ModelSerializer):

    class Meta:
        model = VisitaVendedor
        fields = '__all__'
        # read_only_fields = ('id',)