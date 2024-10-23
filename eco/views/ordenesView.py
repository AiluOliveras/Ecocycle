from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Ordenes, Puntos
from ..serializers import OrdenesSerializer
from rest_framework.permissions import IsAuthenticated


class OrdenesList(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        objetos = Ordenes.objects.filter(reservado=False)
        serializer = OrdenesSerializer(objetos, many=True)
        return Response(serializer.data)

class OrdenReservaUpdate(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        #Parámetros:
        ##pk: id de la orden | ?proveedor_id=<num> :id del proveedor

        #Validación de la orden y sus parametros
        try:
            instance = Ordenes.objects.get(pk=pk)
        except Ordenes.DoesNotExist:
            return Response({'error': 'La orden no existe.'}, status=status.HTTP_404_NOT_FOUND)

        if instance.reservado:
            return Response({'error': 'La orden ya se encuentra reservada.'}, status=status.HTTP_404_NOT_FOUND)

        #Validación del proveedor/punto y sus parámetros
        proveedor_id = request.query_params.get('proveedor_id', None)
        if not proveedor_id:
            return Response({'error': 'Debe identificar su proveedor para poder reservar una orden.'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            Puntos.objects.get(id=proveedor_id)
        except Puntos.DoesNotExist:
            return Response({'error': 'El proveedor no existe en el sistema.'}, status=status.HTTP_404_NOT_FOUND)

        # Marcamos la orden como reservada y registramos quién la reservó
        instance.reservado=True
        instance.proveedor_id=proveedor_id

        instance.save()

        return Response('La orden fué reservada exitosamente', status=status.HTTP_200_OK)

class OrdenEntregaUpdate(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        #Parámetros:
        ##pk: id de la orden 

        # Validación de la orden y sus parametros
        try:
            instance = Ordenes.objects.get(pk=pk)
        except Ordenes.DoesNotExist:
            return Response({'error': 'La orden no existe.'}, status=status.HTTP_404_NOT_FOUND)

        if instance.entregado:
            return Response({'error': 'La orden ya fué entregada anteriormente.'}, status=status.HTTP_202_ACCEPTED)

        # Marcamos la orden como entregada
        instance.entregado=True
        instance.save()

        return Response('La orden se registró como entregada exitosamente', status=status.HTTP_200_OK)


    

