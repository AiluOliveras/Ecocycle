from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Puntos,Tiposmateriales
from ..serializers import PuntosSerializer
from rest_framework.permissions import IsAuthenticated

class PuntoMaterialRegistro(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        #Parámetros:
        ##?deposito_id=<id> :Id del Depósito | ?material=<material> :String material

        #Validacion de la info del punto de recolección
        deposito_id = request.query_params.get('deposito_id', None)
        if not deposito_id:
            return Response({'error': 'Debe identificar su depósito para poder reservar una orden.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            instance = Puntos.objects.get(pk=deposito_id)
        except Puntos.DoesNotExist:
            return Response({'error': 'El punto de recolección de existe.'}, status=status.HTTP_404_NOT_FOUND)

        #Validacion del material
        material_str = request.query_params.get('material', None)
        if not material_str:
            return Response({'error': 'Debe identificar el material a registrar.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            tipo_material=Tiposmateriales.objects.get(nombre=material_str)
        except Tiposmateriales.DoesNotExist:
            return Response({'error': 'El material indicado no existe.'}, status=status.HTTP_404_NOT_FOUND)

        #Validamos que no esté cargado el punto para ese material
        if instance.materiales_posibles.contains(tipo_material):
            return Response({'error': 'El material indicado ya fué registrado para este punto.'}, status=status.HTTP_202_ACCEPTED)

        #Seteamos pivot e/ deposito y material
        instance.materiales_posibles.add(tipo_material)

        return Response('Se dió de alta al depósito como proveedor del material indicado.', status=status.HTTP_200_OK)
