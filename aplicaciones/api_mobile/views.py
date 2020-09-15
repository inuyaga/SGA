from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from aplicaciones.empresa.models import Cliente
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets
from aplicaciones.api_mobile.serializers import VisitaVendedorSerializer
from aplicaciones.plan_de_trabajo.models import VisitaVendedor

# Create your views here.
class GetClienteInfo(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    
    def get(self, request, *args, **kwargs):
        id = kwargs.get('cliente')
        
        estado_respuesta = status.HTTP_200_OK
        content={}
        try:
            cliente = Cliente.objects.get(cli_clave=id)
            if cliente.cli_vndedor_asignado == None:
                estado_respuesta = status.HTTP_204_NO_CONTENT  
            else:
                content = {            
                'clienteID': cliente.cli,
                'cliente': cliente.cli_clave,
                'nombre': cliente.cli_nombre,    
                'rfc': cliente.cli_rfc,    
                'vendedor': cliente.cli_vndedor_asignado.id,    
                }
            
            print(content)
        except ObjectDoesNotExist as error:     
            estado_respuesta = status.HTTP_204_NO_CONTENT                        
        return Response(content, status=estado_respuesta)


 

class VisitaVendedorView(generics.CreateAPIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny] 
    serializer_class = VisitaVendedorSerializer
    queryset = VisitaVendedor.objects.all()

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        IDCliente=request.data["cliente_clave"]
        cliente = Cliente.objects.get(cli_clave=IDCliente)
        request.data["vv_vendedor"]=cliente.cli_vndedor_asignado.id
        request.data["vv_cliente"]=cliente.cli

        
        
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)