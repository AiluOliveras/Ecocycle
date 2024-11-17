from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView

from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from ..models import Punto_recoleccion

class RecicladoresList(ListView):
    model = User
    paginate_by = 10

    ordering = ['username']

    def get_queryset(self):
        punto= self.request.GET.get("punto")
        if punto:
            punto = Punto_recoleccion.objects.get(id=punto)
            queryset = punto.recicladores.all() # Tomo los recicladores asignados al punto

            return queryset

    def get_context_data(self, **kwargs):
        context = super(RecicladoresList, self).get_context_data(**kwargs) # GET de la data default del contexto
        punto= self.request.GET.get("punto")

        context['punto_obj'] = Punto_recoleccion.objects.get(id=punto) # Agrego punto de recoleccion seleccionado al contexto

        return context