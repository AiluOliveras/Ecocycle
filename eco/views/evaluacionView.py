from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from ..models import Evaluacion, Informes, Materiales, Formularios
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
from django.db.models import Sum


def hacer_evaluacion(request, *args, **kwargs):
    """ Genera un registro de evaluaciones con los informes de las últimas dos semanas.

    """

    if request.user.is_staff:

        #Abro comunicación con Bonita
        access = Access(request.user.username)
        access.login()  # Login to get the token
        bonita_process = Process(access)

        #Busco el proceso y lo instancio, es automatico asi que no debo hacer nada mas
        process_id = bonita_process.getProcessId('Proceso de evaluacion de recolectores')
        response = bonita_process.initiateProcess(process_id)

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

        return HttpResponseRedirect('/evaluar/'+str(evaluacion.id))

    return HttpResponse("Hubo un error, por favor regrese a la página anterior.")

class EvaluacionDetail(DetailView):
    model = Evaluacion

    def get_context_data(self, **kwargs):
        context = super(EvaluacionDetail, self).get_context_data(**kwargs) # GET de la data default del contexto
        
        #filtramos data
        #data empleado
        if (self.request.user.is_staff):
            evaluacion_id = self.kwargs['pk']

            #obtengo todos los informes de esa evaluacion
            informes = Informes.objects.filter(evaluacion_id=evaluacion_id)

            cmf=0
            kft=0
            cme=0
            cmnr=0
            mp=0
            kgr=0 #kg de material recibido
            for inf in informes:
                #sumar cantidades ded las 2 semanas
                cmf=cmf+inf.cant_materiales_fallidos
                kft=kft+inf.kg_faltantes_total
                cme=cme+inf.cant_materiales_exitosos
                cmnr=cmnr+inf.cant_mats_no_recibidos
                mp=mp+inf.monto_pagado

                #CANT KG RECIBIDOS
                #obtengo su formulario de mats
                formu_id= (Formularios.objects.get(informe_id=inf.id)).id
                #por cada material recibido,sumo su cantidad
                aux=Materiales.objects.filter(formulario_id=formu_id,material_recibido=True).aggregate(Sum('cantidad'))['cantidad__sum']
                if aux:
                    kgr=kgr+aux
                aux=0


            context['cant_materiales_fallidos'] = cmf
            context['kg_faltantes_total'] = kft
            context['cant_materiales_exitosos'] = cme
            context['cant_mats_no_recibidos'] = cmnr
            context['monto_pagado'] = mp
            context['evaluacion'] = (Evaluacion.objects.latest('id'))

            #porcentaje exitosos
            total_count=informes.count()
            total_exitosos=Informes.objects.filter(cant_materiales_fallidos=0,cant_mats_no_recibidos=0,evaluacion_id=evaluacion_id).count()
            porcen_exit=total_exitosos* 100 / total_count
            context['porcen_entregas_exitosas'] = round(porcen_exit)

            #cantidad kg recibido
            context['cantidad_kg_recibidos']=kgr
            context['precio_por_kg']=round(mp/kgr)
            
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