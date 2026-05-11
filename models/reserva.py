# ============================================================
# MÓDULO: Reserva
# PROYECTO: Sistema Integral de Gestión - Software FJ
# AUTOR: César David Toro Fernández
# DESCRIPCIÓN: Entidad que integra Cliente y Servicio en una
#              reserva completa con ciclo de vida controlado,
#              manejo robusto de excepciones y registro de
#              eventos en el sistema de logs centralizado.
# ============================================================

from datetime import datetime
from models.entidad import Entidad
from models.cliente import Cliente
from models.servicio import Servicio
from exceptions.custom import (
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    DuracionInvalidaError,
    ServicioNoDisponibleError
)
from services.logger import Logger


class Reserva(Entidad):
    """
    Entidad central del sistema que vincula un Cliente con un
    Servicio específico. Gestiona el ciclo de vida completo de
    la reserva: pendiente → confirmada → cancelada, con validaciones
    estrictas y registro detallado de cada transición de estado.
    """

    # Estados válidos del ciclo de vida de una reserva
    ESTADO_PENDIENTE   = "pendiente"
    ESTADO_CONFIRMADA  = "confirmada"
    ESTADO_CANCELADA   = "cancelada"

    _logger = Logger()

    def __init__(self, reserva_id: int, cliente: Cliente,
                 servicio: Servicio, duracion: int):
        """
        Inicializa la reserva vinculando cliente, servicio y duración.

        Args:
            reserva_id: Identificador único de la reserva.
            cliente:    Instancia válida de Cliente registrado.
            servicio:   Instancia válida de Servicio disponible.
            duracion:   Duración del servicio en horas.

        Raises:
            ReservaInvalidaError:      Si cliente o servicio son inválidos.
            DuracionInvalidaError:     Si la duración no supera validación.
            ServicioNoDisponibleError: Si el servicio está deshabilitado.
        """
        try:
            if not isinstance(cliente, Cliente):
                raise ReservaInvalidaError("El cliente proporcionado no es una instancia válida.")
            if not isinstance(servicio, Servicio):
                raise ReservaInvalidaError("El servicio proporcionado no es una instancia válida.")
            if not servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{servicio.nombre}' no está disponible para reservas."
                )
            if not servicio.validar_parametros(duracion):
                raise DuracionInvalidaError(
                    f"Duración inválida: {duracion}h para el servicio '{servicio.nombre}'."
                )

            super().__init__(reserva_id)

            self.__cliente    = cliente
            self.__servicio   = servicio
            self.__duracion   = duracion
            self.__estado     = self.ESTADO_PENDIENTE
            self.__fecha      = datetime.now()
            self.__costo      = servicio.calcular_costo(duracion)

            self._logger.info(
                f"Reserva #{reserva_id} creada | "
                f"Cliente: {cliente.get_nombre()} {cliente.get_apellido()} | "
                f"Servicio: {servicio.nombre} | "
                f"Duración: {duracion}h | Costo: ${self.__costo:,.0f} COP"
            )

        except (ReservaInvalidaError, DuracionInvalidaError, ServicioNoDisponibleError) as e:
            self._logger.error(f"Error al crear reserva #{reserva_id}: {e.mensaje}")
            raise

    # -------------------------------------------------------
    # PROPIEDADES — Acceso controlado al estado de la reserva
    # -------------------------------------------------------

    @property
    def cliente(self) -> Cliente:
        """Retorna la instancia del cliente asociado a la reserva."""
        return self.__cliente

    @property
    def servicio(self) -> Servicio:
        """Retorna la instancia del servicio asociado a la reserva."""
        return self.__servicio

    @property
    def duracion(self) -> int:
        """Retorna la duración en horas de la reserva."""
        return self.__duracion

    @property
    def estado(self) -> str:
        """Retorna el estado actual del ciclo de vida de la reserva."""
        return self.__estado

    @property
    def costo(self) -> float:
        """Retorna el costo total calculado de la reserva."""
        return self.__costo

    @property
    def fecha(self) -> datetime:
        """Retorna la fecha y hora de creación de la reserva."""
        return self.__fecha

    # -------------------------------------------------------
    # CICLO DE VIDA — Transiciones de estado de la reserva
    # -------------------------------------------------------

    def confirmar(self):
        """
        Confirma la reserva transicionando al estado confirmada.

        Raises:
            OperacionNoPermitidaError: Si la reserva no está en estado pendiente.
        """
        try:
            if self.__estado != self.ESTADO_PENDIENTE:
                raise OperacionNoPermitidaError(
                    f"No se puede confirmar una reserva en estado '{self.__estado}'. "
                    f"Solo se pueden confirmar reservas en estado '{self.ESTADO_PENDIENTE}'."
                )
            self.__estado = self.ESTADO_CONFIRMADA
            self._logger.info(
                f"Reserva #{self._id} confirmada | "
                f"Cliente: {self.__cliente.get_nombre()} | "
                f"Costo final: ${self.__costo:,.0f} COP"
            )
        except OperacionNoPermitidaError as e:
            self._logger.error(f"Error al confirmar reserva #{self._id}: {e.mensaje}")
            raise

    def cancelar(self):
        """
        Cancela la reserva transicionando al estado cancelada.

        Raises:
            OperacionNoPermitidaError: Si la reserva ya fue cancelada previamente.
        """
        try:
            if self.__estado == self.ESTADO_CANCELADA:
                raise OperacionNoPermitidaError(
                    f"La reserva #{self._id} ya se encuentra cancelada."
                )
            self.__estado = self.ESTADO_CANCELADA
            self._logger.warning(
                f"Reserva #{self._id} cancelada | "
                f"Cliente: {self.__cliente.get_nombre()} | "
                f"Servicio: {self.__servicio.nombre}"
            )
        except OperacionNoPermitidaError as e:
            self._logger.error(f"Error al cancelar reserva #{self._id}: {e.mensaje}")
            raise

    def procesar(self, descuento: float = 0.0) -> float:
        """
        Procesa la reserva confirmada aplicando descuento opcional.

        Args:
            descuento: Porcentaje de descuento a aplicar (0-100). Por defecto 0.

        Returns:
            Costo final procesado en pesos colombianos (COP).

        Raises:
            OperacionNoPermitidaError: Si la reserva no está confirmada.
            ReservaInvalidaError:      Si ocurre un error durante el procesamiento.
        """
        try:
            if self.__estado != self.ESTADO_CONFIRMADA:
                raise OperacionNoPermitidaError(
                    f"Solo se pueden procesar reservas confirmadas. "
                    f"Estado actual: '{self.__estado}'."
                )
            if descuento > 0:
                self.__costo = self.__servicio.calcular_costo_con_descuento(
                    self.__duracion, descuento
                )
            self._logger.info(
                f"Reserva #{self._id} procesada exitosamente | "
                f"Descuento: {descuento}% | Costo final: ${self.__costo:,.0f} COP"
            )
            return self.__costo

        except OperacionNoPermitidaError as e:
            self._logger.error(f"Error al procesar reserva #{self._id}: {e.mensaje}")
            raise
        except Exception as e:
            error = ReservaInvalidaError(f"Error inesperado procesando reserva #{self._id}: {str(e)}")
            self._logger.error(error.mensaje)
            raise error from e

    # -------------------------------------------------------
    # SERIALIZACIÓN — Representación estructurada del objeto
    # -------------------------------------------------------

    def to_dict(self) -> dict:
        """Serializa la reserva completa a un diccionario de datos."""
        return {
            "id":       self._id,
            "cliente":  self.__cliente.to_dict(),
            "servicio": self.__servicio.to_dict(),
            "duracion": self.__duracion,
            "estado":   self.__estado,
            "costo":    self.__costo,
            "fecha":    self.__fecha.strftime("%Y-%m-%d %H:%M:%S")
        }

    def __str__(self) -> str:
        return (
            f"Reserva #{self._id} | "
            f"{self.__cliente.get_nombre()} {self.__cliente.get_apellido()} | "
            f"{self.__servicio.nombre} | "
            f"{self.__duracion}h | ${self.__costo:,.0f} COP | "
            f"Estado: {self.__estado.upper()}"
        )