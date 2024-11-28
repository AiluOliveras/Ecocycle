from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from ..models import Solicitudes_red
from django.contrib.auth.models import User
import requests

from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
#from ..forms import SolicitantesForm
from django.http import HttpResponseRedirect, HttpResponse

from eco.bonita.access import Access
from eco.bonita.process import Process

from ..views.formulariosView import reservar_stock
from ..models import Tiposmateriales



class Solicitudes_redList(ListView):
    model = Solicitudes_red
    paginate_by = 15

    ordering = ['-id']

    def get_queryset(self):
        return Solicitudes_red.objects.all()

def aprobar_solicitud(request, *args, **kwargs):
    """ Aprueba una solicitud.

    Args:
        punto: id del punto de recolección a verificar

    """

    if request.user.is_staff:
        solicitud= request.GET.get("solicitud")

        if solicitud:
            
            #Busco la solicitud
            solicitud_a_aprobar = Solicitudes_red.objects.get(id=solicitud)

            #ME conecto a la API
            url = "https://ecocycle-tuj9.onrender.com/api/token/"
            payload = {
                "username": "admin",
                "password": "admin123"
                }        
            response = requests.post(url, json=payload)
            
            
            # Si puedo conectarme a la API
            if response.status_code == 200:  # Código 200 significa éxito
                headers = {"Authorization": f"Bearer {response.json()['access']}"}
                #Averiguo mi ID
                nombre_deposito = "Punto Norte"
                url = "https://ecocycle-tuj9.onrender.com/api/get_deposito_by_name/Punto%20Norte/"
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    id_deposito = response.json()["id"]
                    print(f"ID de la solicitud {solicitud_a_aprobar.id_externo} y del deposito {id_deposito}")
                    url = f"https://ecocycle-tuj9.onrender.com/api/reservar_orden/{solicitud_a_aprobar.id_externo}/?proveedor_id={id_deposito}"
                    print(f"URL: {url}")
                    response = requests.post(url, headers=headers)

                    print("SALIDA DE LA RESERVA", response)

                    #Abro comunicación con Bonita
                    access = Access(request.user.username)
                    access.login()  # Login to get the token
                    bonita_process = Process(access)

                    ##Busco todas las tareas activas
                    tareas = bonita_process.getUserTask()
                    #Me quedo con la que me corresponde
                    filtered_task = [task for task in tareas if task['displayName'] == 'Se toma el pedido']
                    print(filtered_task)
                     #Me quedo con el case id
                    if not filtered_task:
                        messages.error(request,('Ningun proceso activo'))

                        return HttpResponseRedirect('/solicitudes_red/')
                    case_id = filtered_task[0]['caseId']
                    print("CASE ID", case_id)

                    # Si pude reservar la orden
                    if response.status_code == 200:
                        
                        #Seteo la variable del proceso
                        respuesta = bonita_process.setVariableByCase(case_id, 'sigueDisponible', "true", 'Boolean')
                        print("Respuesta de setVariableByCase:", respuesta)
                        messages.success(request,('La orden se reservo exitosamente!'))

                        #Seteo la solicitud como aprobada
                        solicitud_a_aprobar.estado = "A"
                        solicitud_a_aprobar.save()

                        #Doy por completada la tarea "SE toma el pedido"
                        task_id = filtered_task[0]['id']             
                        print(f"ID {task_id}")  
                        respuesta = bonita_process.completeActivity(task_id)
                        print(f"SALIDA DEL COMPLETE ACTIVITY {respuesta}")

                        #Disminuyo el stock
                        reservar_stock(solicitud_a_aprobar.tipo_material, solicitud_a_aprobar.cantidad)
                        print("STOCK DISMINUIDO DE LA ORDEN RESERVADA")

                        #Chequeo si ya trabaje con el material
                        material = Tiposmateriales.objects.get(id=solicitud_a_aprobar.tipo_material.id)
                        if material.trabajado:
                            variable_seteada = bonita_process.setVariableByCase(case_id, 'operaMaterial', "false", 'Boolean')
                        else: 
                            variable_seteada = bonita_process.setVariableByCase(case_id, 'operaMaterial', "true", 'Boolean')
                        print("Respuesta de setVariableByCase:", variable_seteada.json())

                        #Doy por completada la tarea "SE carga la orden de distribucion"
                        task_data = bonita_process.searchActivityByCase(case_id)
                        task_id = next((task['id'] for task in task_data if task['displayName'] == 'Se carga la orden de distribución'), None)
                        respuesta = bonita_process.completeActivity(task_id)
                        print(f"SALIDA DEL COMPLETE ACTIVITY {respuesta}")

                    #Si ya estaba reservada
                    elif response.status_code == 202:
                        #Seteo la solicitud como rechazada
                        solicitud_a_aprobar.estado = "R"
                        solicitud_a_aprobar.save()

                        #Seteo la variable del proceso
                        respuesta = bonita_process.setVariableByCase(case_id, 'sigueDisponible', "false", 'Boolean')
                        print("Respuesta de setVariableByCase:", respuesta)

                        messages.error(request,('La orden ya se encontraba reservada'))

                        #Doy por completada la tarea "SE toma el pedido"
                        task_id = filtered_task[0]['id']
                        print(f"ID {id}")             
                        respuesta = bonita_process.completeActivity(task_id)
                        print(f"SALIDA DEL COMPLETE ACTIVITY {respuesta}")

                else:
                    messages.error(request,('No existe el punto en el sistema'))

            else:
                messages.error(request,('Fallo la comunicacion con el sistema'))


            
            
            return HttpResponseRedirect('/solicitudes_red/')
    
    return HttpResponse("Hubo un error, por favor regrese a la página anterior.")