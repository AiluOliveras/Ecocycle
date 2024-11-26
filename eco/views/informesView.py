from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from ..models import Informes, Formularios
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

            messages.success(request,('Se ha marcado como: Pagado.'))
            
            return HttpResponseRedirect('/formularios/detalle/'+str(formulario_id))
    
    return HttpResponse("Hubo un error, por favor regrese a la página anterior.")

