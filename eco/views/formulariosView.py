from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from ..models import Formularios, Materiales, Procesos

from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
#from ..forms import FormulariosForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from ..forms import FormulariosForm
from django.http import HttpResponseRedirect, HttpResponse

from eco.bonita.access import Access
from eco.bonita.process import Process

class FormulariosDetail(DetailView):
    model = Formularios

    def get_context_data(self, **kwargs):
        context = super(FormulariosDetail, self).get_context_data(**kwargs) # GET de la data default del contexto
        
        #agregamos su listado de materiales ya cargados al context
        context['materiales'] = Materiales.objects.filter(formulario_id=(self.kwargs['pk']),material_recibido=False).order_by('id')

        context['materiales_recibidos'] = Materiales.objects.filter(formulario_id=(self.kwargs['pk']),material_recibido=True).order_by('id')

        return context

class FormulariosCreate(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = FormulariosForm
    success_message = 'Formulario creado exitosamente!'
    permission_required = 'add_formularios'
    
    def get_success_url(self):
        return reverse('inicio')
    
    def get_context_data(self, **kwargs):
        context = super(FormulariosCreate, self).get_context_data(**kwargs) # GET de la data default del contexto
        if (self.request.user.is_staff):
            #si es staff del centro de recolección

            #veo si mando el param # de form
            numero = self.request.GET.get('numero',None)
            if numero:
                context['ultimos_formularios'] = Formularios.objects.filter(id__icontains=numero).order_by('-id')[:10]
            else: #mando los ultimos forms
                try:
                    context['ultimo_formulario'] = Formularios.objects.filter(abierto=False).latest('id')
                except Formularios.DoesNotExist:
                    context['ultimo_formulario'] = None
                
                context['ultimos_formularios'] = Formularios.objects.filter(abierto=False).order_by('-id')[:10]

        else:
            #es reciclador
            try:
                context['ultimo_formulario'] = Formularios.objects.filter(abierto=True,reciclador_id=self.request.user.id).latest('id') # Trae el último form creado
            except Formularios.DoesNotExist:
                context['ultimo_formulario'] = None
        return context

    def form_valid(self, form):
        #Si el formulario de carga es válido, guarda el objeto.
        form.instance.reciclador_id = self.request.user.id
        self.object = form.save()

        #AGREGO CALL A BONITA: SE CREA UN FORMULARIO.
            
        return super().form_valid(form)


def cerrar_formulario(request, *args, **kwargs):
    """ Cierra un formulario para que ya no permita la carga de materiales.

    Args:
        formulario: FK con tabla formularios, es el form a cerrar.

    Returns:
        Redirección hacia el inicio del sistema.
    
    """

    formulario= request.GET.get("formulario")
    if formulario:
        #Abro comunicación con Bonita
        access = Access(request.user.username)
        access.login()  # Login to get the token
        bonita_process = Process(access)

        #busco el form
        formulario_up = Formularios.objects.get(id=formulario)
        #seteo el atributo
        formulario_up.abierto=False
        #guardo
        formulario_up.save()        

        #Busco el proceso y lo instancio
        process_id = bonita_process.getProcessId('Proceso de recolección de materiales')
        response = bonita_process.initiateProcess(process_id)
        #Me quedo con el ID de la instancia
        case_id = response['caseId']
        #Checkeo la instancia
        bonita_process.checkCase(case_id)

        # Crear y guardar el proceso en la base de datos
        nuevo_proceso = Procesos(
            iniciado_por=request.user,  # Usuario que inició el proceso
            id_bonita=case_id,  # ID de Bonita (caseId)
            formulario=formulario_up  # Relación con el formulario cerrado
        )
        nuevo_proceso.save()
        
        # #Busco en que tarea me encuentro
        # task_data = bonita_process.searchActivityByCase(case_id)

        # #La doy por completada
        # task_id = task_data[0]['id'] 
        
        # Complete the activity => No es necesario, las tareas automaticas, en este caso guardar en la base de datos, lo hace automaticamente
        # Si mando esta solicitud, da como completa entrega de los materiales
        #respuesta = bonita_process.completeActivity(task_id)
        #print(f"SALIDA DEL COMPLETE ACTIVITY {respuesta}")
        return HttpResponseRedirect('/inicio')
    
    return HttpResponse("Hubo un error, por favor regrese a la página anterior.")