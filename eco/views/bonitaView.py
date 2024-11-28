from rest_framework.views import APIView
from rest_framework.response import Response
import requests

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

                    puedo_cubrir = False # Chequear si puedo cubrir
                    print(f"Devuelvo hayDisponibles {hay_disponibles} y puedoCubrir {puedo_cubrir}")
                    return Response({"hayDisponibles": hay_disponibles, "puedoCubrir": puedo_cubrir})

                return Response(response.json()) 
            else:
                return Response({"error": f"Error en la solicitud: {response.status_code}"})
        else:
            return Response({"error": f"Error en la solicitud: {response.status_code}"})