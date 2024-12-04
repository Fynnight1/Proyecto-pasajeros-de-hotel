from modelo.reserva import Reserva
from modelo.conexion import obtener_conexion

class ReservaController:
    def _init_(self):
        self.conexion = obtener_conexion()
    
    def crear_reserva(self, cliente_id, habitacion_id, trabajador_id, fecha_ingreso, fecha_salida):
        with self.conexion.cursor() as cursor:
            cursor.execute("""
                INSERT INTO reserva (cliente_id, habitacion_id, trabajador_id, fecha_ingreso, fecha_salida)
                VALUES (%s, %s, %s, %s, %s) RETURNING id
            """, (cliente_id, habitacion_id, trabajador_id, fecha_ingreso, fecha_salida))
            id_nueva = cursor.fetchone()[0]
            self.conexion.commit()
            return Reserva(id_nueva, cliente_id, habitacion_id, trabajador_id, fecha_ingreso, fecha_salida)
    
    def obtener_reservas(self):
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT id, cliente_id, habitacion_id, trabajador_id, fecha_ingreso, fecha_salida FROM reserva")
            registros = cursor.fetchall()
            reservas = [Reserva(*registro) for registro in registros]
            return reservas
    
    def actualizar_reserva(self, id, cliente_id, habitacion_id, trabajador_id, fecha_ingreso, fecha_salida):
        with self.conexion.cursor() as cursor:
            cursor.execute("""
                UPDATE reserva
                SET cliente_id=%s, habitacion_id=%s, trabajador_id=%s, fecha_ingreso=%s, fecha_salida=%s
                WHERE id=%s
            """, (cliente_id, habitacion_id, trabajador_id, fecha_ingreso, fecha_salida, id))
            self.conexion.commit()
    
    def eliminar_reserva(self, id):
        with self.conexion.cursor() as cursor:
            cursor.execute("DELETE FROM reserva WHERE id=%s", (id,))
            self.conexion.commit()