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

        return super().form_valid(form)


class Materiales_RecibidosCreate(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = MaterialesForm
    success_message = 'Material cargado exitosamente!'
    permission_required = 'add_materiales'


    def get_context_data(self, **kwargs):
        context = super(Materiales_RecibidosCreate, self).get_context_data(**kwargs) # GET de la data default del contexto
        form_id=self.request.GET.get('form_id', None) #get id de la url
        if form_id:
            #obtengo materiales recibidos
            mats=Materiales.objects.filter(formulario_id=form_id,material_recibido=True)

            tipo_mats_cargados=[] #lista de tipos de materiales cargados
            for mat in mats:
                tipo_mats_cargados.append(mat.tipo_id)

            #retorno materiales que faltan cargar
            context['tiposmateriales'] = Tiposmateriales.objects.exclude(id__in=tipo_mats_cargados)
        else:
            context['tiposmateriales'] = Tiposmateriales.objects.all() # Agrego listado de tipos al contexto
        return context

    def form_valid(self, form):
        #Si el formulario de carga es válido, guarda el material.
        self.object = form.save()

        #Agregamos el material al formulario semanal.
        form_id=self.request.GET.get('form_id', None) #get id de la url
        if (form_id):
            self.object.formulario_id=form_id
            self.object.material_recibido=True

        return super().form_valid(form)

