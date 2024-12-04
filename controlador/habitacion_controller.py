from modelo.habitacion import Habitacion
from modelo.conexion import obtener_conexion

class HabitacionController:
    def _init_(self):
        self.conexion = obtener_conexion()
    
    def crear_habitacion(self, numero, piso, estado, hotel_id):
        with self.conexion.cursor() as cursor:
            cursor.execute("""
                INSERT INTO habitacion (numero, piso, estado, hotel_id)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (numero, piso, estado, hotel_id))
            id_nueva = cursor.fetchone()[0]
            self.conexion.commit()
            return Habitacion(id_nueva, numero, piso, estado, hotel_id)
    
    def obtener_habitaciones(self):
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT id, numero, piso, estado, hotel_id FROM habitacion")
            registros = cursor.fetchall()
            habitaciones = [Habitacion(*registro) for registro in registros]
            return habitaciones
    
    def actualizar_habitacion(self, id, numero, piso, estado, hotel_id):
        with self.conexion.cursor() as cursor:
            cursor.execute("""
                UPDATE habitacion
                SET numero=%s, piso=%s, estado=%s, hotel_id=%s
                WHERE id=%s
            """, (numero, piso, estado, hotel_id, id))
            self.conexion.commit()
    
    def eliminar_habitacion(self, id):
        with self.conexion.cursor() as cursor:
            cursor.execute("DELETE FROM habitacion WHERE id=%s", (id,))
            self.conexion.commit()