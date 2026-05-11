# ============================================================
# MÓDULO: Servicio Abstracto Base
# PROYECTO: Sistema Integral de Gestión - Software FJ
# AUTOR: César David Toro Fernández
# DESCRIPCIÓN: Clase abstracta que define el contrato base
#              para todos los servicios especializados del
#              sistema, implementando polimorfismo estructural.
# ============================================================

from abc import abstractmethod
from models.entidad import Entidad
from exceptions.custom import ServicioNoDisponibleError
from services.logger import Logger


class Servicio(Entidad):
    """
    Clase abstracta que representa un servicio ofrecido por
    Software FJ. Define la interfaz polimórfica que los tres
    servicios especializados deben implementar obligatoriamente.
    """

    _logger = Logger()

    def __init__(self, servicio_id: int, nombre: str, precio_base: float):
        """
        Inicializa el servicio con sus atributos fundamentales.

        Args:
            servicio_id:  Identificador único del servicio.
            nombre:       Nombre descriptivo del servicio.
            precio_base:  Tarifa base en pesos colombianos (COP).

        Raises:
            ServicioNoDisponibleError: Si el precio base es inválido.
        """
        super().__init__(servicio_id)

        try:
            if not nombre or not isinstance(nombre, str):
                raise ServicioNoDisponibleError("El nombre del servicio no puede estar vacío.")
            if not isinstance(precio_base, (int, float)) or precio_base <= 0:
                raise ServicioNoDisponibleError(f"Precio base inválido: '{precio_base}'. Debe ser un valor positivo.")

            self._nombre      = nombre.strip()
            self._precio_base = float(precio_base)
            self._disponible  = True

            self._logger.info(f"Servicio inicializado: {nombre} | Precio base: ${precio_base:,.0f} COP")

        except ServicioNoDisponibleError as e:
            self._logger.error(f"Error al inicializar servicio '{nombre}': {e.mensaje}")
            raise

    # -------------------------------------------------------
    # PROPIEDADES — Acceso controlado a atributos del servicio
    # -------------------------------------------------------

    @property
    def nombre(self) -> str:
        """Retorna el nombre descriptivo del servicio."""
        return self._nombre

    @property
    def precio_base(self) -> float:
        """Retorna la tarifa base del servicio."""
        return self._precio_base

    @property
    def disponible(self) -> bool:
        """Retorna el estado de disponibilidad del servicio."""
        return self._disponible

    def deshabilitar(self):
        """Marca el servicio como no disponible en el sistema."""
        self._disponible = False
        self._logger.warning(f"Servicio deshabilitado: {self._nombre} | ID={self._id}")

    def habilitar(self):
        """Reactiva un servicio previamente deshabilitado."""
        self._disponible = True
        self._logger.info(f"Servicio reactivado: {self._nombre} | ID={self._id}")

    # -------------------------------------------------------
    # MÉTODOS ABSTRACTOS — Contrato polimórfico obligatorio
    # -------------------------------------------------------

    @abstractmethod
    def calcular_costo(self, duracion: int) -> float:
        """
        Calcula el costo total del servicio según su duración.

        Args:
            duracion: Tiempo de uso en horas.

        Returns:
            Costo total calculado en pesos colombianos (COP).
        """
        pass

    @abstractmethod
    def calcular_costo_con_descuento(self, duracion: int, descuento: float) -> float:
        """
        Calcula el costo total aplicando un porcentaje de descuento.

        Args:
            duracion:  Tiempo de uso en horas.
            descuento: Porcentaje de descuento a aplicar (0-100).

        Returns:
            Costo total con descuento en pesos colombianos (COP).
        """
        pass

    @abstractmethod
    def describir(self) -> str:
        """
        Retorna una descripción técnica completa del servicio.

        Returns:
            Cadena descriptiva con características del servicio.
        """
        pass

    @abstractmethod
    def validar_parametros(self, duracion: int) -> bool:
        """
        Valida que los parámetros de uso del servicio sean correctos.

        Args:
            duracion: Tiempo de uso en horas a validar.

        Returns:
            True si los parámetros son válidos, False en caso contrario.
        """
        pass

    # -------------------------------------------------------
    # SERIALIZACIÓN — Representación estructurada del objeto
    # -------------------------------------------------------

    def to_dict(self) -> dict:
        """Serializa el servicio a un diccionario de datos."""
        return {
            "id":          self._id,
            "nombre":      self._nombre,
            "precio_base": self._precio_base,
            "disponible":  self._disponible
        }

    def __str__(self) -> str:
        estado = "Disponible" if self._disponible else "No disponible"
        return f"Servicio #{self._id} | {self._nombre} | ${self._precio_base:,.0f} COP | {estado}"