from .indexView import index
from .materialesView import MaterialesCreate, Materiales_RecibidosCreate
from .formulariosView import FormulariosDetail, FormulariosCreate, cerrar_formulario
from .ordenesView import OrdenesList,OrdenReservaUpdate, OrdenEntregaUpdate
from .puntosView import PuntoMaterialRegistro
from .punto_recoleccionView import Punto_recoleccionCreate, Punto_recoleccionList, create_reciclador_punto, destroy_reciclador_punto, Punto_recoleccion_recicladorList, verificar_punto
from .usuariosView import UsuariosList
from .recicladoresView import RecicladoresList