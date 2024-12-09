# script_crear_admin.py

from modelo.database import Database
from controlador.usuario_controller import UsuarioController

def crear_admin():
    # Inicializar la conexión a la base de datos
    Database.initialize(
        user="postgres",           # Reemplaza con tu usuario de PostgreSQL
        password="Admin1234",      # Reemplaza con tu contraseña de PostgreSQL
        host="localhost",
        port="5432",
        database="hotel_reservation_db"
    )
    
    controller = UsuarioController()
    
    # Datos del administrador a crear
    nombre = "Hernan Espinoza"
    rut = "56555666-7"  # Reemplaza con un RUT válido y único
    direccion = "Calle Administrador 1"
    telefono = "111111111"
    username = "hernan"
    password = "admin123"  # La contraseña será encriptada por el controlador
    rol = "trabajador"
    
    # Crear un administrador
    try:
        admin = controller.crear_usuario(nombre, rut, direccion, telefono, username, password, rol)
        print(f"Administrador creado exitosamente con ID: {admin.id}")
    except Exception as e:
        print(f"Error al crear el administrador: {str(e)}")
    finally:
        # Cerrar todas las conexiones a la base de datos
        Database.close_all_connections()

if __name__ == "__main__":
    crear_admin()
