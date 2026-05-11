# ============================================================
# EXCEPCIONES PERSONALIZADAS - Software FJ
# Autor: César David Toro Fernández
# ============================================================

class SoftwareFJError(Exception):
    """Excepción base del sistema"""
    def __init__(self, mensaje):
        super().__init__(mensaje)
        self.mensaje = mensaje

class ClienteInvalidoError(SoftwareFJError):
    """Error cuando los datos del cliente son inválidos"""
    pass

class ServicioNoDisponibleError(SoftwareFJError):
    """Error cuando un servicio no está disponible"""
    pass

class ReservaInvalidaError(SoftwareFJError):
    """Error cuando una reserva no puede procesarse"""
    pass

class ParametroFaltanteError(SoftwareFJError):
    """Error cuando falta un parámetro obligatorio"""
    pass

class DuracionInvalidaError(SoftwareFJError):
    """Error cuando la duración es inválida"""
    pass

class OperacionNoPermitidaError(SoftwareFJError):
    """Error cuando se intenta una operación no permitida"""
    pass