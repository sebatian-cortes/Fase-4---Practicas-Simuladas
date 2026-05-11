# ============================================================
# MÓDULO: Logger del Sistema
# PROYECTO: Sistema Integral de Gestión - Software FJ
# AUTOR: César David Toro Fernández
# DESCRIPCIÓN: Gestión centralizada de registros de eventos
#              y errores del sistema mediante archivo de logs.
# ============================================================

import os
from datetime import datetime


class Logger:
    """
    Servicio singleton de logging que registra eventos y errores
    del sistema en un archivo de texto plano con marca temporal.
    """

    _instancia = None
    _ruta_log = "Data/logs.txt"

    def __new__(cls):
        # Patrón Singleton: garantiza una única instancia del logger
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia

    def _inicializar(self):
        """Inicializa el directorio y archivo de logs si no existen."""
        os.makedirs("Data", exist_ok=True)
        if not os.path.exists(self._ruta_log):
            with open(self._ruta_log, "w", encoding="utf-8") as f:
                f.write("=" * 60 + "\n")
                f.write("  SISTEMA DE LOGS - SOFTWARE FJ\n")
                f.write("=" * 60 + "\n\n")

    def _escribir(self, nivel: str, mensaje: str):
        """
        Escribe una entrada formateada en el archivo de logs.
        
        Args:
            nivel: Severidad del evento (INFO, ERROR, WARNING).
            mensaje: Descripción detallada del evento registrado.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entrada = f"[{timestamp}] [{nivel}] {mensaje}\n"

        try:
            with open(self._ruta_log, "a", encoding="utf-8") as f:
                f.write(entrada)
        except Exception as e:
            print(f"❌ Error crítico en Logger: {e}")

    def info(self, mensaje: str):
        """Registra un evento informativo exitoso."""
        self._escribir("INFO", mensaje)

    def error(self, mensaje: str):
        """Registra un error detectado en el sistema."""
        self._escribir("ERROR", mensaje)

    def warning(self, mensaje: str):
        """Registra una advertencia de operación sospechosa."""
        self._escribir("WARNING", mensaje)