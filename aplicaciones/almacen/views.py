
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets

# Create your views here.
class CreatePedido(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    
    def get(self, request, *args, **kwargs):
        id = kwargs.get('cliente')
        
        estado_respuesta = status.HTTP_200_OK
        content={}                   
        return Response(content, status=estado_respuesta)
    def post(self, request, *args, **kwargs):

        print(request.data)
        
        estado_respuesta = status.HTTP_200_OK
        content={}                   
        return Response(content, status=estado_respuesta)