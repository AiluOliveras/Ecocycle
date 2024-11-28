from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from ..models import Formularios, Materiales, Procesos, Informes, Stock, Evaluacion

from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
from ..forms import FormulariosForm
from django.http import HttpResponseRedirect, HttpResponse

from eco.bonita.access import Access
from eco.bonita.process import Process
from datetime import datetime, timedelta

class FormulariosDetail(DetailView):
    model = Formularios

    def get_context_data(self, **kwargs):
        context = super(FormulariosDetail, self).get_context_data(**kwargs) # GET de la data default del contexto
         #Busco el proceso para saber el estado y para obtener el número de caso en Bonita
        proceso = Procesos.objects.filter(formulario=self.kwargs['pk']).first() 
        if proceso and proceso.estado == "cerrado":
            #Abro comunicación con Bonita
            access = Access(self.request.user.username)
            access.login()  # Login to get the token
            bonita_process = Process(access)

            #Busco en que tarea me encuentro, para este punto deberia estar en Notificar al recolector de la paga a recibir
            task_data = bonita_process.searchActivityByCase(proceso.id_bonita)
            print(f"DATA DE LA TAREA {task_data}")
            #La doy por completada
            #TENGO QUE FILTRAR PORQUE EN ESTE PUNTO TENGO DOS TAREAS PARALELAS
            task_id = next((task['id'] for task in task_data if task['type'] == 'USER_TASK'), None)
            print(f"ID DE LA TAREA A COMPLETAR {task_id}")
            respuesta = bonita_process.completeActivity(task_id)
            print(f"SALIDA DEL COMPLETE ACTIVITY {respuesta}")

            #Pongo el estado del proceso como entregado
            proceso.estado = 'notificado'
            proceso.save()

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

            ##AÑADO EVALUACION AL CONTEXT - empleado
            fecha_hoy = datetime.now()
            #fecha dos semanas atras
            fecha_dos_semanas = fecha_hoy - timedelta(weeks=2)
            
            #por cada busco evaluac en el periodo, asigno evaluacion_id
            try:
                evaluacion=Evaluacion.objects.latest('id')
            except Evaluacion.DoesNotExist:
                evaluacion=None

            if evaluacion:
                context['evaluacion'] = evaluacion

        else:
            #es reciclador
            try:
                context['ultimo_formulario'] = Formularios.objects.filter(abierto=True,reciclador_id=self.request.user.id).latest('id') # Trae el último form creado
            except Formularios.DoesNotExist:
                context['ultimo_formulario'] = None

            ##AÑADO EVALUACION AL CONTEXT - reciclador
            fecha_hoy = datetime.now()
            #fecha dos semanas atras
            fecha_dos_semanas = fecha_hoy - timedelta(weeks=2)
            
            #por cada busco evaluac en el periodo, asigno evaluacion_id
            try:
                evaluacion=Evaluacion.objects.latest('id')
            except Evaluacion.DoesNotExist:
                evaluacion=None

            if evaluacion:
                context['evaluacion'] = evaluacion

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

        #Busco en que tarea me encuentro, para este punto deberia estar en Entrega de los materiales
        task_data = bonita_process.searchActivityByCase(nuevo_proceso.id_bonita)
        print(f"DATA DE LA TAREA {task_data}")
        #La doy por completada
        task_id = task_data[0]['id']             
        respuesta = bonita_process.completeActivity(task_id)
        print(f"SALIDA DEL COMPLETE ACTIVITY {respuesta}")

        #Pongo el estado del proceso como entregado
        nuevo_proceso.estado = 'entregado'
        nuevo_proceso.save()
        
        return HttpResponseRedirect('/inicio')
    
    return HttpResponse("Hubo un error, por favor regrese a la página anterior.")

def actualizar_stock(id_tipo,cantidad_agregada): #actualiza el stock sumando la cantidad enviada por parametro

    try:
        stock=Stock.objects.get(tipo_material_id=id_tipo)
    except Stock.DoesNotExist:
        Stock.objects.create(tipo_material_id=id_tipo,cantidad=cantidad_agregada)
        return True
    
    #existe el tipo en la bd, sumo cantidades
    stock.cantidad= stock.cantidad+cantidad_agregada
    stock.save()

    return True

def reservar_stock(id_tipo,cantidad_reservada): #actualiza el stock restando la cantidad enviada por parametro

    try:
        stock=Stock.objects.get(tipo_material_id=id_tipo)
    except Stock.DoesNotExist:
        Stock.objects.create(tipo_material_id=id_tipo,cantidad=cantidad_reservada)
        return True
    
    #existe el tipo en la bd, resto cantidades
    stock.cantidad= stock.cantidad-cantidad_reservada
    stock.save()

    return True

def consultar_stock(id_tipo): #recibe un id y retorna el stock que hay de ese tipo_material. Si no hay existencias del material enviado, retorna None.

    try:
        stock=Stock.objects.get(tipo_material_id=id_tipo)
    except Stock.DoesNotExist:
        return None

    return stock.cantidad

def procesar_diferencias_formulario(request, *args, **kwargs):
    """ Procesa diferencias entre los materiales cargados por el reciclador y el empleado.

    Args:
        formulario_id: id del formulario a procesar

    """

    if request.user.is_staff:
        formulario_id= request.GET.get("formulario_id")
        
        #variables de bi
        materiales_faltantes=0 #materiales faltantes o que trajo menos cantidad (total tipos material)
        kg_faltantes_total=0 #cantidades de kg de material faltante
        materiales_exitosos=0 #cumplio cantidades
        tipo_mats_recibidos=[]
        pago_total=0

        if formulario_id:
            #Abro comunicación con Bonita
            access = Access(request.user.username)
            access.login()  # Login to get the token
            bonita_process = Process(access)

            #Busco el proceso para obtener el número de caso en Bonita
            proceso = Procesos.objects.get(formulario=formulario_id)

            form = Formularios.objects.get(id=formulario_id)
            materiales_cargados = Materiales.objects.filter(formulario_id=formulario_id,material_recibido=False)
            materiales_recibidos = Materiales.objects.filter(formulario_id=formulario_id,material_recibido=True)

            # #Busco en que tarea me encuentro, para este punto deberia estar en Carga los materiales en un formulario del sistema
            task_data = bonita_process.searchActivityByCase(proceso.id_bonita)
            print(f"DATA DE LA TAREA {task_data}")
            # #La doy por completada
            task_id = task_data[0]['id']             
            respuesta = bonita_process.completeActivity(task_id)
            print(f"SALIDA DEL COMPLETE ACTIVITY {respuesta}")
            proceso.estado = 'cerrado'
            proceso.save()

            for material_r in materiales_recibidos:
                #busco su equivalente en cargados
                total_material=0 #total de cada material cargado
                tipo_mats_recibidos.append(material_r.tipo_id)
                pago_total=pago_total+(material_r.cantidad * material_r.tipo.precio_por_kg)

                #ACTUALIZA STOCK
                actualizar_stock(material_r.tipo_id,material_r.cantidad)

                for material_c in materiales_cargados:
                    if material_c.tipo_id == material_r.tipo_id:
                        #es el mismo material
                        total_material=total_material+material_c.cantidad #sumo cantidad de ese material
                
                if material_r.cantidad < total_material:
                    #si la cantidad total de material recibido es MENOR al material cargado

                    #registro error
                    kg_faltantes_total=kg_faltantes_total+(total_material-material_r.cantidad)
                    materiales_faltantes=materiales_faltantes+1

                else:
                    #trajo la misma o mas cantidad
                    materiales_exitosos=materiales_exitosos+1

            #verifico que materiales cargo y no recibi
            mats_no_recibidos = (Materiales.objects.filter(formulario_id=formulario_id,material_recibido=False)).exclude(tipo_id__in=tipo_mats_recibidos)
            tipo_mats_no_recibidos= []

            if mats_no_recibidos:
                #faltan materiales
                for m in mats_no_recibidos:

                    #si no existe en tipo_mats_no_recibidos
                    if m.tipo_id not in tipo_mats_no_recibidos:
                        #lo agrego
                        tipo_mats_no_recibidos.append(m.tipo_id)
                        kg_faltantes_total=kg_faltantes_total+m.cantidad #cuento los kg del material no traido, al total
                        materiales_faltantes=materiales_faltantes+1

            #termino comparaciones
            # print('materiales faltantes/fallidos (en total):'+str(materiales_faltantes))
            # print('kg faltantes:'+str(kg_faltantes_total))
            # print('mats exitosos:'+str(materiales_exitosos))
            # print('mats no recibidos (faltan por completo):'+str(len(mats_no_recibidos)))

            #guardo en db  
            nuevo_informe=Informes.objects.create(cant_materiales_fallidos=materiales_faltantes,kg_faltantes_total=kg_faltantes_total,cant_materiales_exitosos=materiales_exitosos,cant_mats_no_recibidos=len(mats_no_recibidos),monto_pagado=pago_total)          
            form.informe_id=nuevo_informe.id #conecto formulario a informe
            form.save()

            ##LLAMADO A BONITA !!!!!!!!!!!!!!!!
            ##COMPUERTA / Consulta api
            #Utilizar consultas: actualizar_stock , reservar_stock y consultar_stock en este mismo file
            #ejemplo de llamada: actualizar_stock(material.tipo_id,material.cantidad)
            #mas info en el encabezado de cada función
            
            messages.success(request,('Procesado exitosamente!'))
            
            return HttpResponseRedirect('/formularios/detalle/'+str(formulario_id))
    
    return HttpResponse("Hubo un error, por favor regrese a la página anterior.")