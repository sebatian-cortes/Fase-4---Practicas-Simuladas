from .UserService import UserService



class UserController:

    def __init__(self):
        self.service = UserService()

    # ==========================
    # CREAR USUARIO
    # ==========================
    def crear_usuario(self, data):

        required_fields = ["name", "lastname", "phone", "email"]

        for field in required_fields:

            if field not in data:
                return {"error": f"Falta el campo {field}"}

        return self.service.crear_usuario(
            data["name"],
            data["lastname"],
            data["phone"],
            data["email"]
        )

    # ==========================
    # OBTENER USUARIO
    # ==========================
    def obtener_usuario(self, name):

        if not name:
            return {"error": "Debe ingresar un nombre"}

        return self.service.obtener_usuario_por_nombre(name)