import datetime
from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from ..models import Informes, Formularios, Procesos
from django.contrib.auth.models import User

from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
#from ..forms import Punto_recoleccionForm
from django.http import HttpResponseRedirect, HttpResponse

from eco.bonita.access import Access
from eco.bonita.process import Process

def marcar_informe_pagado(request, *args, **kwargs):
    """ Marca un informe como pagado.

    Args:
        formulario_id: Id de la tabla formularios.

    """

    if request.user.is_staff:

        formulario_id= request.GET.get("formulario_id")

        if formulario_id:
            #busco el form
            try:
                informe_id= (Formularios.objects.get(id=formulario_id)).informe_id
            except Exception as e:
                return HttpResponse("Hubo un error, por favor regrese a la página anterior.")

            #se asigna el punto
            informe = Informes.objects.get(id=informe_id)
            informe.pagado=True
            informe.save()

            proceso = Procesos.objects.get(formulario=formulario_id)
            if proceso.estado == "notificado":
                #Abro comunicación con Bonita
                access = Access(request.user.username)
                access.login()  # Login to get the token
                bonita_process = Process(access)

                #Busco en que tarea me encuentro, para este punto deberia estar en Notificar al recolector de la paga a recibir
                task_data = bonita_process.searchActivityByCase(proceso.id_bonita)
                print(f"DATA DE LA TAREA {task_data}")
                #La doy por completada
                task_id = task_data[0]['id']             
                respuesta = bonita_process.completeActivity(task_id)
                print(f"SALIDA DEL COMPLETE ACTIVITY {respuesta}")

                #Pongo el estado del proceso como entregado
                proceso.estado = 'pagado'
                proceso.fin = datetime.datetime.now()
                proceso.save()

            messages.success(request,('Se ha marcado como: Pagado.'))
            
            return HttpResponseRedirect('/formularios/detalle/'+str(formulario_id))
    
    return HttpResponse("Hubo un error, por favor regrese a la página anterior.")
