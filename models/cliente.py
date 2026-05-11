# ============================================================
# MÓDULO: Cliente
# PROYECTO: Sistema Integral de Gestión - Software FJ
# AUTOR: César David Toro Fernández
# DESCRIPCIÓN: Entidad Cliente con encapsulamiento estricto,
#              validaciones robustas y manejo de excepciones
#              personalizadas sobre cada campo de datos.
# ============================================================

from models.entidad import Entidad
from exceptions.custom import ClienteInvalidoError
from services.logger import Logger


class Cliente(Entidad):
    """
    Representa un cliente registrado en el sistema Software FJ.
    Hereda de Entidad e implementa encapsulamiento total sobre
    sus atributos, con validaciones estrictas en cada setter.
    """

    _logger = Logger()

    def __init__(self, cliente_id: int, nombre: str, apellido: str,
                 telefono: str, email: str):
        """
        Inicializa un cliente validando todos sus campos.

        Args:
            cliente_id: Identificador único del cliente.
            nombre:     Nombre del cliente (solo caracteres alfabéticos).
            apellido:   Apellido del cliente (solo caracteres alfabéticos).
            telefono:   Teléfono de contacto (solo dígitos numéricos).
            email:      Correo electrónico con formato válido.

        Raises:
            ClienteInvalidoError: Si algún campo no supera la validación.
        """
        super().__init__(cliente_id)
        self.set_nombre(nombre)
        self.set_apellido(apellido)
        self.set_telefono(telefono)
        self.set_email(email)
        self._logger.info(f"Cliente registrado exitosamente: {nombre} {apellido} | ID={cliente_id}")

    # -------------------------------------------------------
    # GETTERS — Acceso controlado a los atributos privados
    # -------------------------------------------------------

    def get_nombre(self) -> str:
        return self.__nombre

    def get_apellido(self) -> str:
        return self.__apellido

    def get_telefono(self) -> str:
        return self.__telefono

    def get_email(self) -> str:
        return self.__email

    # -------------------------------------------------------
    # SETTERS — Mutación con validación estricta por campo
    # -------------------------------------------------------

    def set_nombre(self, nombre: str):
        """Valida que el nombre sea una cadena alfabética no vacía."""
        try:
            if not nombre or not isinstance(nombre, str):
                raise ClienteInvalidoError("El nombre no puede estar vacío.")
            if not nombre.replace(" ", "").isalpha():
                raise ClienteInvalidoError(f"Nombre inválido: '{nombre}'. Solo se permiten letras.")
            self.__nombre = nombre.strip()
        except ClienteInvalidoError as e:
            self._logger.error(f"Validación fallida en nombre: {e.mensaje}")
            raise

    def set_apellido(self, apellido: str):
        """Valida que el apellido sea una cadena alfabética no vacía."""
        try:
            if not apellido or not isinstance(apellido, str):
                raise ClienteInvalidoError("El apellido no puede estar vacío.")
            if not apellido.replace(" ", "").isalpha():
                raise ClienteInvalidoError(f"Apellido inválido: '{apellido}'. Solo se permiten letras.")
            self.__apellido = apellido.strip()
        except ClienteInvalidoError as e:
            self._logger.error(f"Validación fallida en apellido: {e.mensaje}")
            raise

    def set_telefono(self, telefono: str):
        """Valida que el teléfono contenga únicamente dígitos numéricos."""
        try:
            if not telefono or not telefono.isdigit():
                raise ClienteInvalidoError(f"Teléfono inválido: '{telefono}'. Solo se permiten dígitos.")
            self.__telefono = telefono.strip()
        except ClienteInvalidoError as e:
            self._logger.error(f"Validación fallida en teléfono: {e.mensaje}")
            raise

    def set_email(self, email: str):
        """Valida que el email contenga el símbolo @ y un dominio."""
        try:
            if not email or "@" not in email or "." not in email.split("@")[-1]:
                raise ClienteInvalidoError(f"Email inválido: '{email}'.")
            self.__email = email.strip().lower()
        except ClienteInvalidoError as e:
            self._logger.error(f"Validación fallida en email: {e.mensaje}")
            raise

    # -------------------------------------------------------
    # SERIALIZACIÓN — Representación estructurada del objeto
    # -------------------------------------------------------

    def to_dict(self) -> dict:
        """Serializa el cliente a un diccionario de datos."""
        return {
            "id":       self._id,
            "nombre":   self.__nombre,
            "apellido": self.__apellido,
            "telefono": self.__telefono,
            "email":    self.__email
        }

    def __str__(self) -> str:
        return f"Cliente #{self._id} | {self.__nombre} {self.__apellido} | {self.__email}"