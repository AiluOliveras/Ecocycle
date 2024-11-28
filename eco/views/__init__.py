from .indexView import index
from .materialesView import MaterialesCreate, Materiales_RecibidosCreate
from .formulariosView import FormulariosDetail, FormulariosCreate, cerrar_formulario, procesar_diferencias_formulario
from .ordenesView import OrdenesList,OrdenReservaUpdate, OrdenEntregaUpdate
from .puntosView import PuntoMaterialRegistro
from .punto_recoleccionView import Punto_recoleccionCreate, Punto_recoleccionList, create_reciclador_punto, destroy_reciclador_punto, Punto_recoleccion_recicladorList, verificar_punto
from .usuariosView import UsuariosList
from .recicladoresView import RecicladoresList
from .informesView import marcar_informe_pagado
from .bonitaView import ConsultaBonita
from .evaluacionView import hacer_evaluacion, EvaluacionDetail
from .solicitantesView import SolicitantesCreate,SolicitantesList, SolicitantesDelete, create_reciclador
from .solicitudes_redView import Solicitudes_redList, aprobar_solicitud
from .bonitaView import ConsultaBonita