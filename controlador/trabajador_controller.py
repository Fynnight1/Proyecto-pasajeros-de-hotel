from modelo.trabajador import Trabajador
from modelo.conexion import obtener_conexion

class TrabajadorController:
    def _init_(self):
        self.conexion = obtener_conexion()
    
    def crear_trabajador(self, nombre, rut, direccion, telefono, hotel_id):
        with self.conexion.cursor() as cursor:
            cursor.execute("""
                INSERT INTO trabajador (nombre, rut, direccion, telefono, hotel_id)
                VALUES (%s, %s, %s, %s, %s) RETURNING id
            """, (nombre, rut, direccion, telefono, hotel_id))
            id_nuevo = cursor.fetchone()[0]
            self.conexion.commit()
            return Trabajador(id_nuevo, nombre, rut, direccion, telefono, hotel_id)
    
    def obtener_trabajadores(self):
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, rut, direccion, telefono, hotel_id FROM trabajador")
            registros = cursor.fetchall()
            trabajadores = [Trabajador(*registro) for registro in registros]
            return trabajadores
    
    def actualizar_trabajador(self, id, nombre, rut, direccion, telefono, hotel_id):
        with self.conexion.cursor() as cursor:
            cursor.execute("""
                UPDATE trabajador
                SET nombre=%s, rut=%s, direccion=%s, telefono=%s, hotel_id=%s
                WHERE id=%s
            """, (nombre, rut, direccion, telefono, hotel_id, id))
            self.conexion.commit()
    
    def eliminar_trabajador(self, id):
        with self.conexion.cursor() as cursor:
            cursor.execute("DELETE FROM trabajador WHERE id=%s", (id,))
            self.conexion.commit()