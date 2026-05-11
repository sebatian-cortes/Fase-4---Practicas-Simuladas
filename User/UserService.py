from .User import User

class UserService:

    def __init__(self):
        self.users = []
        self.current_id = 1

    # ==========================
    # CARGAR USUARIOS DESDE TXT
    # ==========================
    def cargar_usuarios(self, ruta_archivo):

        try:
            with open(ruta_archivo, "r") as archivo:

                for linea in archivo:

                    datos = linea.strip().split(",")

                    user = User(
                        self.current_id,
                        datos[0],  # name
                        datos[1],  # lastname
                        datos[2],  # phone
                        datos[3],  # email
                        datos[4]   # estado
                    )

                    self.users.append(user)
                    self.current_id += 1

            print("✅ Usuarios cargados correctamente")

        except FileNotFoundError:
            print("❌ Archivo no encontrado")

        except Exception as e:
            print("❌ Error cargando usuarios:", e)

    # ==========================
    # CREAR USUARIO
    # ==========================
    def crear_usuario(self, name, lastname, phone, email):

        try:
            user = User(
                self.current_id,
                name,
                lastname,
                phone,
                email,
                "usuario"
            )

            self.users.append(user)
            self.current_id += 1

            return user.to_dict()

        except Exception as e:
            return {"error": str(e)}

    # ==========================
    # BUSCAR USUARIO POR NOMBRE
    # ==========================
    def obtener_usuario_por_nombre(self, name):

        try:
            for user in self.users:

                if user.get_name().lower() == name.lower():
                    return user.to_dict()

            return {"error": "Usuario no encontrado"}

        except Exception as e:
            return {"error": str(e)}