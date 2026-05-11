class User:
    def __init__(self, user_id, name, lastname, phone, email, estado):
        self.__id = user_id
        self.set_name(name)
        self.set_lastname(lastname)
        self.set_phone(phone)
        self.set_email(email)
        self.set_estado(estado)

 
    # GETTERS, son los metodos que nos permitiran traer los datos para consultas en la app
   

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_lastname(self):
        return self.__lastname

    def get_phone(self):
        return self.__phone

    def get_email(self):
        return self.__email

    def get_estado(self):
        return self.__estado

   
    # SETTERS, nos permitiran actulizar los campos a excepcion del id que no debe ser modidficado
 

    def set_name(self, name):
        if not name or not isinstance(name, str):
            raise ValueError("Nombre inválido")
        self.__name = name

    def set_lastname(self, lastname):
        if not lastname or not isinstance(lastname, str):
            raise ValueError("Apellido inválido")
        self.__lastname = lastname

    def set_phone(self, phone):
        if not phone.isdigit():
            raise ValueError("Teléfono inválido")
        self.__phone = phone

    def set_email(self, email):
        if "@" not in email:
            raise ValueError("Email inválido")
        self.__email = email

    def set_estado(self, estado):
        if estado.lower() not in ["usuario", "cliente"]:
            raise ValueError("Estado debe ser 'usuario' o 'cliente'")
        self.__estado = estado.lower()

  
    # este metodo nos permitira dejar mas claros los logs en su archivo
  

    def to_dict(self):
        """Convertir a diccionario (útil para logs o mostrar)"""
        return {
            "id": self.__id,
            "name": self.__name,
            "lastname": self.__lastname,
            "phone": self.__phone,
            "email": self.__email,
            "estado": self.__estado
        }

    def __str__(self):
        return f"{self.__name} {self.__lastname} ({self.__estado})"