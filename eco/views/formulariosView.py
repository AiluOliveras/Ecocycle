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


class FormulariosDetail(DetailView):
    model = Formularios

    def get_context_data(self, **kwargs):
        context = super(FormulariosDetail, self).get_context_data(**kwargs) # GET de la data default del contexto
        
        #agregamos su listado de materiales ya cargados al context
        context['materiales'] = Materiales.objects.filter(formulario_id=(self.kwargs['pk'])).order_by('id')

        return context