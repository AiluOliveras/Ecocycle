from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from decimal import Decimal

from eco.views.formulariosView import consultar_stock
from ..models import Tiposmateriales, Solicitudes_red

class ConsultaBonita(APIView):

    #permission_classes = [IsAuthenticated]

    def get(self, request):
        # Seteo los parametros para recibir el token
        url = "https://ecocycle-tuj9.onrender.com/api/token/"
        payload = {
        "username": "admin",
        "password": "admin123"
        }        
        response = requests.post(url, json=payload)
        
        # Si recibo
        if response.status_code == 200:  # Código 200 significa éxito
            # Listo las ordenes
            url = "https://ecocycle-tuj9.onrender.com/api/ordenes_disponibles/"
            headers = {"Authorization": f"Bearer {response.json()['access']}"}
            response = requests.get(url, headers=headers)

            # Si las recibo
            if response.status_code == 200:
                ordenes = response.json()
                hay_disponibles = any(item["reservado"] == False for item in ordenes)

                # Si no hay disponibles, ya devuelvo
                if not hay_disponibles:
                    return Response({"hayDisponibles": hay_disponibles, "puedoCubrir": False})

                # Si hay disponibles, debo chequear si las puedo satisfacer
                else:
                    puedo_cubrir = False # Inicializo en false
                    for orden in ordenes:
                        material = Tiposmateriales.objects.get(nombre=orden["tipo"]["nombre"])
                        stock = consultar_stock(material.id)
                        cantidad_orden = Decimal(orden["cantidad"])
                        if stock and stock >= cantidad_orden:
                            # Crear y guardar la solicitud que puedo cubrir
                            existe = Solicitudes_red.objects.filter(cantidad=cantidad_orden, tipo_material=material, estado="P").exists()

                            if not existe:
                                nueva_solicitud = Solicitudes_red(
                                    cantidad=cantidad_orden, 
                                    tipo_material=material,  
                                    estado="P",
                                    id_externo=orden["id"]
                                )
                                nueva_solicitud.save()
                            if not puedo_cubrir:
                                puedo_cubrir = True
                    
                    print(f"Devuelvo hayDisponibles {hay_disponibles} y puedoCubrir {puedo_cubrir}")
                    return Response({"hayDisponibles": hay_disponibles, "puedoCubrir": puedo_cubrir})

            else:
                return Response({"error": f"Error en la solicitud: {response.status_code}"})
        else:
            return Response({"error": f"Error en la solicitud: {response.status_code}"})