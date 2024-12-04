from modelo.hotel import Hotel
from modelo.conexion import obtener_conexion

class HotelController:
    def _init_(self):
        self.conexion = obtener_conexion()
    
    def crear_hotel(self, nombre, direccion, telefono):
        with self.conexion.cursor() as cursor:
            cursor.execute("""
                INSERT INTO hotel (nombre, direccion, telefono)
                VALUES (%s, %s, %s) RETURNING id
            """, (nombre, direccion, telefono))
            id_nuevo = cursor.fetchone()[0]
            self.conexion.commit()
            return Hotel(id_nuevo, nombre, direccion, telefono)
    
    def obtener_hoteles(self):
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, direccion, telefono FROM hotel")
            registros = cursor.fetchall()
            hoteles = [Hotel(*registro) for registro in registros]
            return hoteles
    
    def actualizar_hotel(self, id, nombre, direccion, telefono):
        with self.conexion.cursor() as cursor:
            cursor.execute("""
                UPDATE hotel
                SET nombre=%s, direccion=%s, telefono=%s
                WHERE id=%s
            """, (nombre, direccion, telefono, id))
            self.conexion.commit()
    
    def eliminar_hotel(self, id):
        with self.conexion.cursor() as cursor:
            cursor.execute("DELETE FROM hotel WHERE id=%s", (id,))
            self.conexion.commit()