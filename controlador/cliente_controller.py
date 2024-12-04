from modelo.cliente import Cliente
from modelo.conexion import obtener_conexion

class ClienteController:
    def _init_(self):
        self.conexion = obtener_conexion()
    
    def crear_cliente(self, nombre, rut, direccion, telefono):
        with self.conexion.cursor() as cursor:
            cursor.execute("""
                INSERT INTO cliente (nombre, rut, direccion, telefono)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (nombre, rut, direccion, telefono))
            id_nuevo = cursor.fetchone()[0]
            self.conexion.commit()
            return Cliente(id_nuevo, nombre, rut, direccion, telefono)
    
    def obtener_clientes(self):
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, rut, direccion, telefono FROM cliente")
            registros = cursor.fetchall()
            clientes = [Cliente(*registro) for registro in registros]
            return clientes
    
    def actualizar_cliente(self, id, nombre, rut, direccion, telefono):
        with self.conexion.cursor() as cursor:
            cursor.execute("""
                UPDATE cliente
                SET nombre=%s, rut=%s, direccion=%s, telefono=%s
                WHERE id=%s
            """, (nombre, rut, direccion, telefono, id))
            self.conexion.commit()
    
    def eliminar_cliente(self, id):
        with self.conexion.cursor() as cursor:
            cursor.execute("DELETE FROM cliente WHERE id=%s", (id,))
            self.conexion.commit()