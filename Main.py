from User.UserService import UserService
from User.UserController import UserController

service = UserService()


service.cargar_usuarios("data/users.txt")


for user in service.users:
    print(user)

controller = UserController()





def pintar_usuario(data):

    if "error" in data:
        print("\n❌", data["error"])
        return

    print("\n✅ Usuario encontrado")
    print(f"ID: {data['id']}")
    print(f"Nombre: {data['name']}")
    print(f"Apellido: {data['lastname']}")
    print(f"Teléfono: {data['phone']}")
    print(f"Email: {data['email']}")
    print(f"Estado: {data['estado']}")





while True:

    print("\n========= MENÚ =========")
    print("1. Crear usuario")
    print("2. Buscar usuario")
    print("3. Salir")

    opcion = input("Seleccione una opción: ")




    if opcion == "1":

        name = input("Nombre: ")
        lastname = input("Apellido: ")
        phone = input("Teléfono: ")
        email = input("Email: ")

        data = {
            "name": name,
            "lastname": lastname,
            "phone": phone,
            "email": email
        }

        respuesta = controller.crear_usuario(data)

        print("\nRespuesta del sistema:")
        pintar_usuario(respuesta)




    elif opcion == "2":

        name = input("Ingrese el nombre del usuario: ")

        respuesta = controller.obtener_usuario(name)

        print("\nRespuesta del sistema:")
        pintar_usuario(respuesta)




    elif opcion == "3":

        print("\n Programa finalizado")
        break

    else:
        print("\n Opción inválida")