from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from ..models import Formularios, Materiales

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
        context['materiales'] = Materiales.objects.filter(formulario_id=(self.kwargs['pk'])).order_by('id')

        return context

class FormulariosCreate(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = FormulariosForm
    success_message = 'Formulario creado exitosamente!'
    permission_required = 'add_formularios'
    
    def get_success_url(self):
        return reverse('inicio')
    
    def get_context_data(self, **kwargs):
        context = super(FormulariosCreate, self).get_context_data(**kwargs) # GET de la data default del contexto
        context['ultimo_formulario'] = Formularios.objects.order_by('id').last() # Trae el último form creado
        return context

    def form_valid(self, form):
        #Si el formulario de carga es válido, guarda el objeto.
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
        access = Access()
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

        #Me traigo todos los materiales cargados en este formulario
        materiales = Materiales.objects.filter(formulario_id=formulario).order_by('id')
        variable_bonita = ""
        #Formateo todos los materiales como un string para mandarselo a Bonita
        for material in materiales:
            if not variable_bonita:
                variable_bonita += f"{material.tipo.nombre}: {material.cantidad}"
            else:
                variable_bonita += f", {material.tipo.nombre}: {material.cantidad}"

        #Seteo la variable del proceso
        respue = bonita_process.setVariableByCase(case_id, 'materiales_cargados', variable_bonita, 'String')
        #Busco en que tarea me encuentro
        task_data = bonita_process.searchActivityByCase(case_id)

        #La doy por completada
        task_id = task_data[0]['id']  # Assuming the first task in the list
        
        # Complete the activity
        respuesta = bonita_process.completeActivity(task_id)
        print(f"SALIDA DEL COMPLETE ACTIVITY {respuesta}")

        return HttpResponseRedirect('/inicio')
    
    return HttpResponse("Hubo un error, por favor regrese a la página anterior.")