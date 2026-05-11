# ============================================================
# MÓDULO: Servicio de Alquiler de Equipos
# PROYECTO: Sistema Integral de Gestión - Software FJ
# AUTOR: César David Toro Fernández
# DESCRIPCIÓN: Servicio especializado para alquiler de equipos
#              tecnológicos de nivel profesional, con cálculo
#              de costos por tipo de equipo y validaciones
#              estrictas sobre disponibilidad y duración.
# ============================================================

from models.servicio import Servicio
from exceptions.custom import DuracionInvalidaError, ServicioNoDisponibleError, ParametroFaltanteError
from services.logger import Logger


class AlquilerEquipo(Servicio):
    """
    Servicio especializado para alquiler de equipos tecnológicos
    de alto rendimiento. Implementa polimorfismo sobre los métodos
    abstractos de Servicio con tarifas diferenciadas por tipo de equipo.
    """

    _logger = Logger()

    # Catálogo de equipos disponibles con sus tarifas por hora en COP
    CATALOGO_EQUIPOS = {
        "laptop":     75000,
        "servidor":  150000,
        "proyector":  45000,
        "camara":     60000,
        "drone":     120000
    }

    DURACION_MINIMA = 1   # horas
    DURACION_MAXIMA = 24  # horas

    def __init__(self, servicio_id: int, tipo_equipo: str, cantidad: int = 1):
        """
        Inicializa el servicio de alquiler con el tipo y cantidad de equipos.

        Args:
            servicio_id:  Identificador único del servicio.
            tipo_equipo:  Tipo de equipo del catálogo disponible.
            cantidad:     Número de unidades a alquilar (mínimo 1).

        Raises:
            ParametroFaltanteError: Si el tipo de equipo no existe en el catálogo.
        """
        try:
            tipo_lower = tipo_equipo.strip().lower()
            if tipo_lower not in self.CATALOGO_EQUIPOS:
                raise ParametroFaltanteError(
                    f"Equipo '{tipo_equipo}' no disponible. "
                    f"Opciones válidas: {', '.join(self.CATALOGO_EQUIPOS.keys())}"
                )
            precio = self.CATALOGO_EQUIPOS[tipo_lower] * max(1, cantidad)
            super().__init__(servicio_id, f"Alquiler de {tipo_equipo.capitalize()}", precio)
            self.__tipo_equipo = tipo_lower
            self.__cantidad    = max(1, cantidad)
            self._logger.info(
                f"Equipo configurado | Tipo: {tipo_equipo} | "
                f"Cantidad: {self.__cantidad} | Tarifa: ${precio:,.0f} COP/hora"
            )
        except ParametroFaltanteError as e:
            Logger().error(f"Error al configurar equipo '{tipo_equipo}': {e.mensaje}")
            raise

    def calcular_costo(self, duracion: int) -> float:
        """
        Calcula el costo total del alquiler según duración en horas.

        Args:
            duracion: Número de horas de alquiler del equipo.

        Returns:
            Costo total en pesos colombianos (COP).

        Raises:
            DuracionInvalidaError:     Si la duración está fuera del rango permitido.
            ServicioNoDisponibleError: Si el servicio está deshabilitado.
        """
        try:
            if not self._disponible:
                raise ServicioNoDisponibleError(f"El equipo '{self.__tipo_equipo}' no está disponible.")
            if not self.validar_parametros(duracion):
                raise DuracionInvalidaError(
                    f"Duración inválida: {duracion}h. Rango permitido: "
                    f"{self.DURACION_MINIMA}-{self.DURACION_MAXIMA} horas."
                )
            costo = self._precio_base * duracion
            self._logger.info(
                f"Costo calculado | {self.__tipo_equipo.capitalize()} x{self.__cantidad} | "
                f"{duracion}h | ${costo:,.0f} COP"
            )
            return costo

        except (DuracionInvalidaError, ServicioNoDisponibleError) as e:
            self._logger.error(f"Error en cálculo de costo de equipo: {e.mensaje}")
            raise

    def calcular_costo_con_descuento(self, duracion: int, descuento: float) -> float:
        """
        Calcula el costo total del alquiler aplicando un descuento porcentual.

        Args:
            duracion:  Número de horas de alquiler.
            descuento: Porcentaje de descuento a aplicar (0-100).

        Returns:
            Costo final con descuento aplicado en COP.
        """
        try:
            if not (0 <= descuento <= 100):
                raise DuracionInvalidaError(f"Descuento inválido: {descuento}%. Debe estar entre 0 y 100.")
            costo_base  = self.calcular_costo(duracion)
            costo_final = costo_base * (1 - descuento / 100)
            self._logger.info(
                f"Descuento aplicado | {self.__tipo_equipo.capitalize()} | "
                f"{descuento}% | ${costo_base:,.0f} → ${costo_final:,.0f} COP"
            )
            return costo_final
        except DuracionInvalidaError as e:
            self._logger.error(f"Error aplicando descuento en equipo: {e.mensaje}")
            raise

    def describir(self) -> str:
        """Retorna descripción técnica completa del servicio de alquiler."""
        return (
            f"Servicio: {self._nombre} | "
            f"Tipo: {self.__tipo_equipo.capitalize()} | "
            f"Cantidad: {self.__cantidad} unidad(es) | "
            f"Tarifa: ${self._precio_base:,.0f} COP/hora | "
            f"Rango: {self.DURACION_MINIMA}-{self.DURACION_MAXIMA} horas"
        )

    def validar_parametros(self, duracion: int) -> bool:
        """Valida que la duración esté dentro del rango permitido."""
        return self.DURACION_MINIMA <= duracion <= self.DURACION_MAXIMA

    def to_dict(self) -> dict:
        """Serializa el servicio de alquiler a un diccionario de datos."""
        base = super().to_dict()
        base["tipo_equipo"] = self.__tipo_equipo
        base["cantidad"]    = self.__cantidad
        return base

    def __str__(self) -> str:
        return (
            f"Alquiler #{self._id} | {self.__tipo_equipo.capitalize()} "
            f"x{self.__cantidad} | ${self._precio_base:,.0f} COP/hora"
        )