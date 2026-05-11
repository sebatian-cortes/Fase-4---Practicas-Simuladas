# ============================================================
# MÓDULO: Servicio de Asesoría Especializada
# PROYECTO: Sistema Integral de Gestión - Software FJ
# AUTOR: César David Toro Fernández
# DESCRIPCIÓN: Servicio especializado para asesorías técnicas
#              y estratégicas en arquitectura de software, con
#              tarifas diferenciadas por nivel de especialización
#              y cálculo de costos con impuestos aplicados.
# ============================================================

from models.servicio import Servicio
from exceptions.custom import DuracionInvalidaError, ServicioNoDisponibleError, ParametroFaltanteError
from services.logger import Logger


class AsesoriaEspecializada(Servicio):
    """
    Servicio especializado para asesorías técnicas y estratégicas.
    Implementa polimorfismo sobre los métodos abstractos de Servicio
    con tarifas escalonadas por nivel y cálculo de costos con IVA.
    """

    _logger = Logger()

    # Niveles de asesoría disponibles con sus tarifas base en COP
    NIVELES = {
        "basico":    120000,
        "avanzado":  250000,
        "experto":   450000
    }

    DURACION_MINIMA = 1  # horas
    DURACION_MAXIMA = 8  # horas
    IVA             = 0.19

    def __init__(self, servicio_id: int, nivel: str, asesor: str):
        """
        Inicializa el servicio de asesoría con nivel y nombre del asesor.

        Args:
            servicio_id: Identificador único del servicio.
            nivel:       Nivel de especialización (basico/avanzado/experto).
            asesor:      Nombre completo del asesor asignado.

        Raises:
            ParametroFaltanteError: Si el nivel no existe en el catálogo.
        """
        try:
            nivel_lower = nivel.strip().lower()
            if nivel_lower not in self.NIVELES:
                raise ParametroFaltanteError(
                    f"Nivel '{nivel}' no válido. "
                    f"Opciones disponibles: {', '.join(self.NIVELES.keys())}"
                )
            precio = self.NIVELES[nivel_lower]
            super().__init__(servicio_id, f"Asesoría {nivel.capitalize()}", precio)
            self.__nivel  = nivel_lower
            self.__asesor = asesor.strip()
            self._logger.info(
                f"Asesoría configurada | Nivel: {nivel} | "
                f"Asesor: {asesor} | Tarifa: ${precio:,.0f} COP/hora"
            )
        except ParametroFaltanteError as e:
            Logger().error(f"Error al configurar asesoría nivel '{nivel}': {e.mensaje}")
            raise

    def calcular_costo(self, duracion: int) -> float:
        """
        Calcula el costo base de la asesoría según duración en horas.

        Args:
            duracion: Número de horas de asesoría requeridas.

        Returns:
            Costo total sin IVA en pesos colombianos (COP).

        Raises:
            DuracionInvalidaError:     Si la duración está fuera del rango permitido.
            ServicioNoDisponibleError: Si el servicio está deshabilitado.
        """
        try:
            if not self._disponible:
                raise ServicioNoDisponibleError(f"La asesoría nivel '{self.__nivel}' no está disponible.")
            if not self.validar_parametros(duracion):
                raise DuracionInvalidaError(
                    f"Duración inválida: {duracion}h. Rango permitido: "
                    f"{self.DURACION_MINIMA}-{self.DURACION_MAXIMA} horas."
                )
            costo = self._precio_base * duracion
            self._logger.info(
                f"Costo calculado | Asesoría {self.__nivel} | "
                f"{duracion}h | ${costo:,.0f} COP (sin IVA)"
            )
            return costo

        except (DuracionInvalidaError, ServicioNoDisponibleError) as e:
            self._logger.error(f"Error en cálculo de costo de asesoría: {e.mensaje}")
            raise

    def calcular_costo_con_descuento(self, duracion: int, descuento: float) -> float:
        """
        Calcula el costo aplicando descuento porcentual sobre la tarifa base.

        Args:
            duracion:  Número de horas de asesoría.
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
                f"Descuento aplicado | Asesoría {self.__nivel} | "
                f"{descuento}% | ${costo_base:,.0f} → ${costo_final:,.0f} COP"
            )
            return costo_final
        except DuracionInvalidaError as e:
            self._logger.error(f"Error aplicando descuento en asesoría: {e.mensaje}")
            raise

    def calcular_costo_con_iva(self, duracion: int) -> float:
        """
        Calcula el costo total de la asesoría incluyendo IVA del 19%.

        Args:
            duracion: Número de horas de asesoría requeridas.

        Returns:
            Costo total con IVA incluido en pesos colombianos (COP).
        """
        try:
            costo_base  = self.calcular_costo(duracion)
            costo_total = costo_base * (1 + self.IVA)
            self._logger.info(
                f"IVA aplicado | Asesoría {self.__nivel} | "
                f"${costo_base:,.0f} + 19% IVA = ${costo_total:,.0f} COP"
            )
            return costo_total
        except Exception as e:
            self._logger.error(f"Error calculando IVA en asesoría: {e}")
            raise

    def describir(self) -> str:
        """Retorna descripción técnica completa del servicio de asesoría."""
        return (
            f"Servicio: {self._nombre} | "
            f"Nivel: {self.__nivel.capitalize()} | "
            f"Asesor: {self.__asesor} | "
            f"Tarifa: ${self._precio_base:,.0f} COP/hora | "
            f"IVA: {int(self.IVA * 100)}% | "
            f"Rango: {self.DURACION_MINIMA}-{self.DURACION_MAXIMA} horas"
        )

    def validar_parametros(self, duracion: int) -> bool:
        """Valida que la duración esté dentro del rango permitido."""
        return self.DURACION_MINIMA <= duracion <= self.DURACION_MAXIMA

    def to_dict(self) -> dict:
        """Serializa el servicio de asesoría a un diccionario de datos."""
        base = super().to_dict()
        base["nivel"]  = self.__nivel
        base["asesor"] = self.__asesor
        base["iva"]    = self.IVA
        return base

    def __str__(self) -> str:
        return (
            f"Asesoría #{self._id} | Nivel: {self.__nivel.capitalize()} | "
            f"Asesor: {self.__asesor} | ${self._precio_base:,.0f} COP/hora"
        )