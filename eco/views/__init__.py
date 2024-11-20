from .indexView import index, bonita
from .materialesView import MaterialesCreate
from .formulariosView import FormulariosDetail, FormulariosCreate, cerrar_formulario
from .ordenesView import OrdenesList,OrdenReservaUpdate, OrdenEntregaUpdate
from .puntosView import PuntoMaterialRegistro
from .punto_recoleccionView import Punto_recoleccionCreate, Punto_recoleccionList, create_reciclador_punto, destroy_reciclador_punto, Punto_recoleccion_recicladorList
from .usuariosView import UsuariosList
from .recicladoresView import RecicladoresList