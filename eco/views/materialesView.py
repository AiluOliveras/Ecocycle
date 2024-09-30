from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView

from eco.bonita.access import Access
from eco.bonita.process import Process
from ..models import Materiales,Tiposmateriales,Formularios

from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from ..forms import MaterialesForm
from django.contrib.auth.mixins import PermissionRequiredMixin

class MaterialesCreate(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = MaterialesForm
    success_message = 'Material cargado exitosamente!'
    permission_required = 'add_materiales'

    # def get_success_url(self):
    #     return reverse('/formularios/detalle/1')

    def get_context_data(self, **kwargs):
        context = super(MaterialesCreate, self).get_context_data(**kwargs) # GET de la data default del contexto
        context['tiposmateriales'] = Tiposmateriales.objects.all() # Agrego listado de tipos al contexto
        return context

    def form_valid(self, form):
        #Si el formulario de carga es válido, guarda el material.
        self.object = form.save()

        #Agregamos el material al formulario semanal.
        form_id=self.request.GET.get('form_id', None) #get id de la url
        if (form_id):
            self.object.formulario_id=form_id
        print(form)
        self.start_bonita_process(form)
        return super().form_valid(form)

    def start_bonita_process(self, form):
         # Initialize Bonita BPM API Access
        access = Access()
        access.login()  # Login to get the token

        # Instantiate the Process class with the access object
        bonita_process = Process(access)

        # Get the Bonita process ID by name
        process_id = bonita_process.getProcessId('Proceso de recolección de materiales')

        # Initiate the process
        response = bonita_process.initiateProcess(process_id)

        # Extract caseId from the response
        case_id = response['caseId']

        # Set the process variables using the form data
        bonita_process.setVariableByCase(case_id, 'cantidad_materiales', form.cleaned_data['cantidad'], 'float')
        bonita_process.setVariableByCase(case_id, 'tipo_material', form.cleaned_data['tipo'].nombre, 'String')

        # Assign the task to a user (e.g., 'bates')
        task_data = bonita_process.searchActivityByCase(case_id)
        print(f"task data: {task_data}")
        task_id = task_data[0]['id']  # Assuming the first task in the list

        # Complete the activity
        bonita_process.completeActivity(task_id)
