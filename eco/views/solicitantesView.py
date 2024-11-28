from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from ..models import Solicitantes, Proceso_solicitante
from django.contrib.auth.models import User

from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
from ..forms import SolicitantesForm
from django.http import HttpResponseRedirect, HttpResponse

from eco.bonita.access import Access
from eco.bonita.process import Process
from ..models import Proceso_solicitante



class SolicitantesCreate(SuccessMessageMixin, CreateView):
    form_class = SolicitantesForm
    success_message = 'Solicitud de registro creada exitosamente!'
    
    def get_success_url(self):
        return reverse('inicio')

    def form_valid(self, form):

        #Abro comunicación con Bonita
        access = Access("solicitante")
        access.login()  # Login to get the token
        bonita_process = Process(access)

        #Busco el proceso y lo instancio
        process_id = bonita_process.getProcessId('Proceso de registro de recolector')
        response = bonita_process.initiateProcess(process_id)
        #Me quedo con el ID de la instancia
        case_id = response['caseId']
        #Checkeo la instancia
        bonita_process.checkCase(case_id)

        # Crear y guardar el proceso en la base de datos
        nuevo_proceso = Proceso_solicitante(
            username=form.instance.username,  # Usuario que inició el proceso
            id_bonita=case_id,  # ID de Bonita (caseId)
        )
        nuevo_proceso.save()

        #Busco en que tarea me encuentro, para este punto deberia estar en Completar formulario
        task_data = bonita_process.searchActivityByCase(nuevo_proceso.id_bonita)
        print(f"DATA DE LA TAREA {task_data}")
        #La doy por completada
        task_id = task_data[0]['id']             
        respuesta = bonita_process.completeActivity(task_id)
        print(f"SALIDA DEL COMPLETE ACTIVITY {respuesta}")

            
        return super().form_valid(form)

class SolicitantesList(ListView):
    model = Solicitantes
    paginate_by = 15

    ordering = ['-id']

    def get_queryset(self):
        return Solicitantes.objects.all()

class SolicitantesDelete(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Solicitantes
    form = SolicitantesForm
    fields = "__all__"
    permission_required = 'delete_solicitantes'

    def get_success_url(self):
        #Abro comunicación con Bonita
        access = Access(self.request.user.username)
        access.login()  # Login to get the token
        bonita_process = Process(access)

        variable_seteada = bonita_process.setVariableByCase(case_id, 'cumpleRequisitos', "true", 'Boolean')
        print("Respuesta de setVariableByCase:", variable_seteada.json())

        success_message = 'Solicitud rechazada.'
        messages.success (self.request, (success_message))
        return reverse('solicitantes')


def create_reciclador(request,pk):
    """ Da de alta un reciclador en la bbdd como usuario al aceptarse la solicitud.

    """

    if request.user.is_staff:
        from django.contrib.auth.models import User

        if pk:

            #busco el solicitante
            solicitante = Solicitantes.objects.get(id=pk)

            #verifica si existe el user
            try:
                user=User.objects.get(username=solicitante.username)
                #el user existe, genero otro username
                ult_id=(User.objects.latest('id')).id
                ult_id=ult_id+1
                solicitante_usuario=(str(solicitante.username)+str(ult_id))
                User.objects.create_user(username=solicitante_usuario,email=solicitante.email,password='123',first_name=solicitante.nombre,last_name=solicitante.apellido,is_superuser=True,is_staff=False)

            except User.DoesNotExist:
                #el username está disponible, crea usuario
                User.objects.create_user(username=solicitante.username,email=solicitante.email,password='123',first_name=solicitante.nombre,last_name=solicitante.apellido,is_superuser=True,is_staff=False)
                
            proceso = Proceso_solicitante.objects.get(username=solicitante.username)

            #Abro comunicación con Bonita
            access = Access(request.user.username)
            access.login()  # Login to get the token
            bonita_process = Process(access)

            variable_seteada = bonita_process.setVariableByCase(proceso.id_bonita, 'cumpleRequisitos', "true", 'Boolean')
            print("Respuesta de setVariableByCase:", variable_seteada)

            task_data = bonita_process.searchActivityByCase(proceso.id_bonita)
            print(f"DATA DE LA TAREA {task_data}")
            #La doy por completada
            task_id = task_data[0]["id"]        
            respuesta = bonita_process.completeActivity(task_id)
            print(f"SALIDA DEL COMPLETE ACTIVITY {respuesta}")


            #borro la solicitud
            Solicitantes.objects.filter(id=pk).delete()

            messages.success(request,('Solicitante creado exitosamente!'))
            
            return HttpResponseRedirect('/solicitudes')
    
    return HttpResponse("Hubo un error, por favor regrese a la página anterior.")