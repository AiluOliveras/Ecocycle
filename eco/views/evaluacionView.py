from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from ..models import Evaluacion, Informes
from django.contrib.auth.models import User
from datetime import datetime, timedelta

from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
#from ..forms import Punto_recoleccionForm
from django.http import HttpResponseRedirect, HttpResponse

from eco.bonita.access import Access
from eco.bonita.process import Process


def hacer_evaluacion(request, *args, **kwargs):
    """ Genera un registro de evaluaciones con los informes de las últimas dos semanas.

    """

    if request.user.is_staff:
        #fecha hoy
        fecha_hoy = datetime.now()
        #fecha dos semanas atras
        fecha_dos_semanas = fecha_hoy - timedelta(weeks=2)

        #creo evaluacion
        evaluacion= Evaluacion.objects.create(fecha_inicio=fecha_dos_semanas)
        
        #por cada informe, asigno evaluacion_id
        infs=Informes.objects.filter(fecha__gte=fecha_dos_semanas, fecha__lte=fecha_hoy)

        for inf in infs:
            #seteo id de evaluacion
            inf.evaluacion_id=evaluacion.id
            inf.save()

        return HttpResponseRedirect('/inicio')

    return HttpResponse("Hubo un error, por favor regrese a la página anterior.")

class EvaluacionDetail(DetailView):
    model = Evaluacion

    def get_context_data(self, **kwargs):
        context = super(EvaluacionDetail, self).get_context_data(**kwargs) # GET de la data default del contexto
        
        #filtramos data
        #data empleado
        if (self.request.user.is_staff):
            print('hola')
        #data reciclador
        else:
            evaluacion_id = self.kwargs['pk']

            #obtengo sus informes de esa evaluacion
            informes = Informes.objects.filter(evaluacion_id=evaluacion_id,formularios__reciclador_id=self.request.user.id)
            
            cmf=0
            kft=0
            cme=0
            cmnr=0
            mp=0
            for inf in informes:
                #sumar cantidades ded las 2 semanas
                cmf=cmf+inf.cant_materiales_fallidos
                kft=kft+inf.kg_faltantes_total
                cme=cme+inf.cant_materiales_exitosos
                cmnr=cmnr+inf.cant_mats_no_recibidos
                mp=mp+inf.monto_pagado

            context['cant_materiales_fallidos'] = cmf
            context['kg_faltantes_total'] = kft
            context['cant_materiales_exitosos'] = cme
            context['cant_mats_no_recibidos'] = cmnr
            context['monto_pagado'] = mp
            context['evaluacion'] = (Evaluacion.objects.latest('id'))

        return context