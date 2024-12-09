# controlador/usuario_controller.py

from modelo.usuario import Usuario

class UsuarioController:
    def crear_usuario(self, nombre, rut, direccion, telefono, username, password, rol):
        return Usuario.crear(nombre, rut, direccion, telefono, username, password, rol)

    def autenticar(self, username, password):
        return Usuario.autenticar(username, password)

    def obtener_usuarios(self):
        return Usuario.obtener_todos()

    def obtener_usuario_por_id(self, usuario_id):
        return Usuario.obtener_por_id(usuario_id)

    def actualizar_usuario(self, usuario_id, nombre=None, rut=None, direccion=None, telefono=None, username=None, password=None, rol=None, activo=None):
        return Usuario.actualizar(usuario_id, nombre, rut, direccion, telefono, username, password, rol, activo)

    def desactivar_usuario(self, usuario_id):
        return Usuario.desactivar(usuario_id)
