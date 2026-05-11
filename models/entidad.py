# ============================================================
# MÓDULO: Entidad Base Abstracta
# PROYECTO: Sistema Integral de Gestión - Software FJ
# AUTOR: César David Toro Fernández
# DESCRIPCIÓN: Clase abstracta raíz que establece el contrato
#              base para todas las entidades del sistema.
# ============================================================

from abc import ABC, abstractmethod


class Entidad(ABC):
    """
    Clase abstracta base del sistema. Define la interfaz mínima
    que toda entidad del dominio debe implementar obligatoriamente.
    Garantiza consistencia estructural en toda la jerarquía de clases.
    """

    def __init__(self, entidad_id: int):
        """
        Inicializa la entidad con un identificador único.

        Args:
            entidad_id: Identificador numérico único de la entidad.
        """
        self._id = entidad_id

    @property
    def id(self):
        """Retorna el identificador único de la entidad."""
        return self._id

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Serializa la entidad a un diccionario de datos.
        Implementación obligatoria en cada clase derivada.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Representación legible de la entidad para logs y consola.
        Implementación obligatoria en cada clase derivada.
        """
        pass

    def __repr__(self):
        """Representación técnica de la entidad para depuración."""
        return f"<{self.__class__.__name__} id={self._id}>"