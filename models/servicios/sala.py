# ============================================================
# MÓDULO: Servicio de Reserva de Salas
# PROYECTO: Sistema Integral de Gestión - Software FJ
# AUTOR: César David Toro Fernández
# DESCRIPCIÓN: Servicio especializado para reserva de salas
#              ejecutivas con cálculo de costos, descuentos
#              y validación estricta de parámetros de uso.
# ============================================================

from models.servicio import Servicio
from exceptions.custom import DuracionInvalidaError, ServicioNoDisponibleError
from services.logger import Logger


class ReservaSala(Servicio):
    """
    Servicio especializado para reserva de salas de reuniones
    de alta tecnología. Implementa polimorfismo sobre los métodos
    abstractos de Servicio con lógica de negocio propia.
    """

    _logger = Logger()

    # Restricciones de negocio para este servicio
    DURACION_MINIMA = 1   # horas
    DURACION_MAXIMA = 12  # horas
    CAPACIDAD_MAX   = 20  # personas

    def __init__(self, servicio_id: int, capacidad: int):
        """
        Inicializa el servicio de sala con su capacidad máxima.

        Args:
            servicio_id: Identificador único del servicio.
            capacidad:   Número máximo de personas permitidas en la sala.
        """
        super().__init__(servicio_id, "Reserva de Sala Ejecutiva", 85000)
        self.__capacidad = min(capacidad, self.CAPACIDAD_MAX)
        self._logger.info(f"Sala ejecutiva configurada | Capacidad: {self.__capacidad} personas")

    def calcular_costo(self, duracion: int) -> float:
        """
        Calcula el costo base de la reserva según duración en horas.

        Args:
            duracion: Número de horas de uso de la sala.

        Returns:
            Costo total en pesos colombianos (COP).

        Raises:
            DuracionInvalidaError:       Si la duración está fuera del rango permitido.
            ServicioNoDisponibleError:   Si el servicio está deshabilitado.
        """
        try:
            if not self._disponible:
                raise ServicioNoDisponibleError("La sala no está disponible actualmente.")
            if not self.validar_parametros(duracion):
                raise DuracionInvalidaError(
                    f"Duración inválida: {duracion}h. Rango permitido: "
                    f"{self.DURACION_MINIMA}-{self.DURACION_MAXIMA} horas."
                )
            costo = self._precio_base * duracion
            self._logger.info(f"Costo calculado | Sala | {duracion}h | ${costo:,.0f} COP")
            return costo

        except (DuracionInvalidaError, ServicioNoDisponibleError) as e:
            self._logger.error(f"Error en cálculo de costo de sala: {e.mensaje}")
            raise

    def calcular_costo_con_descuento(self, duracion: int, descuento: float) -> float:
        """
        Calcula el costo aplicando un porcentaje de descuento.

        Args:
            duracion:  Número de horas de uso.
            descuento: Porcentaje de descuento entre 0 y 100.

        Returns:
            Costo final con descuento aplicado en COP.
        """
        try:
            if not (0 <= descuento <= 100):
                raise DuracionInvalidaError(f"Descuento inválido: {descuento}%. Debe estar entre 0 y 100.")
            costo_base = self.calcular_costo(duracion)
            costo_final = costo_base * (1 - descuento / 100)
            self._logger.info(
                f"Descuento aplicado | Sala | {descuento}% | "
                f"${costo_base:,.0f} → ${costo_final:,.0f} COP"
            )
            return costo_final
        except DuracionInvalidaError as e:
            self._logger.error(f"Error aplicando descuento en sala: {e.mensaje}")
            raise

    def describir(self) -> str:
        """Retorna descripción técnica completa del servicio de sala."""
        return (
            f"Servicio: {self._nombre} | "
            f"Capacidad: {self.__capacidad} personas | "
            f"Tarifa: ${self._precio_base:,.0f} COP/hora | "
            f"Rango: {self.DURACION_MINIMA}-{self.DURACION_MAXIMA} horas"
        )

    def validar_parametros(self, duracion: int) -> bool:
        """Valida que la duración esté dentro del rango permitido."""
        return self.DURACION_MINIMA <= duracion <= self.DURACION_MAXIMA

    def to_dict(self) -> dict:
        """Serializa el servicio de sala a un diccionario de datos."""
        base = super().to_dict()
        base["capacidad"] = self.__capacidad
        return base

    def __str__(self) -> str:
        return f"Sala Ejecutiva #{self._id} | Capacidad: {self.__capacidad} personas | ${self._precio_base:,.0f} COP/hora"