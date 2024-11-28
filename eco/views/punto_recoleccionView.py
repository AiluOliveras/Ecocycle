from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from ..models import Punto_recoleccion, Punto_proceso
from django.contrib.auth.models import User

from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
from ..forms import Punto_recoleccionForm
from django.http import HttpResponseRedirect, HttpResponse

from eco.bonita.access import Access
from eco.bonita.process import Process

from ..models import Proceso_solicitante

class Punto_recoleccionCreate(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = Punto_recoleccionForm
    success_message = 'Punto de recolección creado exitosamente!'
    permission_required = 'add_punto_recoleccion'
    
    def get_success_url(self):
        return reverse('inicio')

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Acceder a la instancia recién creada
        punto_creado = self.object
        
        #Abro comunicación con Bonita
        access = Access(self.request.user.username)
        access.login()  # Login to get the token
        bonita_process = Process(access)

        #Busco el proceso y lo instancio
        process_id = bonita_process.getProcessId('Proceso de alta de un nuevo punto de recolección')
        proceso_iniciado = bonita_process.initiateProcess(process_id)
        #Me quedo con el ID de la instancia
        case_id = proceso_iniciado['caseId']
        # Crear y guardar el proceso en la base de datos
        nuevo_proceso = Punto_proceso(
            iniciado_por=self.request.user,  # Usuario que inició el proceso
            id_bonita=case_id,  # ID de Bonita (caseId)
            punto=punto_creado  # Relación con el formulario cerrado
        )
        nuevo_proceso.save()

        return response

class Punto_recoleccionList(ListView):
    model = Punto_recoleccion
    paginate_by = 15

    ordering = ['-id']

    def get_queryset(self):
        nombre = self.request.GET.get('nombre')
        if nombre:
            return Punto_recoleccion.objects.filter(nombre__icontains=nombre)
        else:
            return Punto_recoleccion.objects.all()

def create_reciclador_punto(request, *args, **kwargs):
    """ Asigna un punto de recolección a un reciclador.

    Args:
        punto: FK con tabla punto recolección, es el punto que se quiere asignar al recolector
        reciclador: FK con tabla usuarios, es el recolector al que se le asigna el punto

    Returns:
        Redirección hacia el template de puntos de recolección con un mensaje de operacion exitosa.
    
    Raises:
        HttpResponse con mensaje de error en caso de ocurrir algun problema de indices.

    """

    if request.user.is_staff:
        from django.contrib.auth.models import User
        reciclador= request.GET.get("reciclador")
        punto= request.GET.get("punto")

        if reciclador and punto:
            #checkear que no exista ya la unión

            #se asigna el punto
            punto_up = Punto_recoleccion.objects.get(id=punto)
            reciclador_up = User.objects.get(id=reciclador)
            punto_up.recicladores.add(reciclador_up)

            try:
                proceso = Proceso_solicitante.objects.get(username=reciclador_up.username)
                #Abro comunicación con Bonita
                access = Access(request.user.username)
                access.login()  # Login to get the token
                bonita_process = Process(access)

                task_data = bonita_process.searchActivityByCase(proceso.id_bonita)
                print(f"DATA DE LA TAREA {task_data}")
                #La doy por completada
                task_id = task_data[0]["id"]        
                respuesta = bonita_process.completeActivity(task_id)
                print(f"SALIDA DEL COMPLETE ACTIVITY {respuesta}")
                # Aquí puedes usar el objeto `proceso` como lo necesites
            except Proceso_solicitante.DoesNotExist:
                # Manejo del caso en que no se encuentre el objeto
                pass


            messages.success(request,('Reciclador añadido exitosamente!'))
            
            return HttpResponseRedirect('/punto_recoleccion/listar/recicladores/?punto='+punto)
    
    return HttpResponse("Hubo un error, por favor regrese a la página anterior.")

def destroy_reciclador_punto(request, *args, **kwargs):
    """ Da de baja a un reciclador de un punto.

    Args:
        punto: FK con tabla punto recoleccion, es el punto sobre el cual se da de baja
        reciclador: FK con tabla usuarios, es el usuario que quiere darse de baja del punto

    Returns:
        Redirección hacia el template de recicladores con un mensaje de operacion exitosa.
    
    Raises:
        HttpResponse con mensaje de error en caso de ocurrir algun problema de indices.

    """

    if request.user.is_staff:
        from django.contrib.auth.models import User
        reciclador= request.GET.get("reciclador")
        punto= request.GET.get("punto")

        if punto and reciclador:

            #se elimina permiso del reciclador sobre el punto dado
            punto_up = Punto_recoleccion.objects.get(id=punto)
            reciclador_up = User.objects.get(id=reciclador)
            punto_up.recicladores.remove(reciclador_up)

            messages.success(request,('Punto removido del reciclador exitosamente!'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) #recargo pag  base

    return HttpResponse("Hubo un error, por favor regrese a la página anterior.")

class Punto_recoleccion_recicladorList(ListView):
    model = Punto_recoleccion
    paginate_by = 30

    ordering = ['nombre']

    def get_queryset(self):
        reciclador= self.request.user.id
        return Punto_recoleccion.objects.filter(recicladores__id=reciclador)

def verificar_punto(request, *args, **kwargs):
    """ Marca un punto de recolección como verificado.

    Args:
        punto: id del punto de recolección a verificar

    """

    if request.user.is_staff:
        punto= request.GET.get("punto")

        if punto:

            punto_up = Punto_recoleccion.objects.get(id=punto)
            punto_up.verificado = True
            punto_up.save()

            #Abro comunicación con Bonita
            access = Access(request.user.username)
            access.login()  # Login to get the token
            bonita_process = Process(access)

            #Busco el punto para obtener el número de caso en Bonita
            proceso = Punto_proceso.objects.get(punto=punto)

            # #Busco en que tarea me encuentro, para este punto deberia estar en Recibe y chequea el alta de un nuevo punto de recoleccion
            task_data = bonita_process.searchActivityByCase(proceso.id_bonita)
            print(f"DATA DE LA TAREA {task_data}")
            case_id = task_data[0]['caseId']
            print("CASE ID", case_id)
            #Seteo la variable del proceso
            respuesta = bonita_process.setVariableByCase(case_id, 'aprueba', "true", 'Boolean')
            print("Respuesta de setVariableByCase:", respuesta)
            #La doy por completada
            task_id = task_data[0]['id']             
            respuesta = bonita_process.completeActivity(task_id)
            print(f"SALIDA DEL COMPLETE ACTIVITY {respuesta}")


            messages.success(request,('Punto verificado exitosamente!'))
            
            return HttpResponseRedirect('/punto_recoleccion/listar/')
    
    return HttpResponse("Hubo un error, por favor regrese a la página anterior.")