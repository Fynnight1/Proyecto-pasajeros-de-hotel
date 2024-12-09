# modelo/reserva.py

from .database import Database

class Reserva:
    def __init__(self, id, cliente_id, habitacion_id, trabajador_id, fecha_ingreso, fecha_salida):
        self.id = id
        self.cliente_id = cliente_id
        self.habitacion_id = habitacion_id
        self.trabajador_id = trabajador_id
        self.fecha_ingreso = fecha_ingreso
        self.fecha_salida = fecha_salida

    @staticmethod
    def crear(cliente_id, habitacion_id, trabajador_id, fecha_ingreso, fecha_salida):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO reserva (cliente_id, habitacion_id, trabajador_id, fecha_ingreso, fecha_salida)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id
                """, (cliente_id, habitacion_id, trabajador_id, fecha_ingreso, fecha_salida))
                reserva_id = cur.fetchone()[0]
                conn.commit()
                return Reserva(reserva_id, cliente_id, habitacion_id, trabajador_id, fecha_ingreso, fecha_salida)
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            Database.return_connection(conn)

    @staticmethod
    def obtener_todas():
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM reserva")
                rows = cur.fetchall()
                return [Reserva(*row) for row in rows]
        finally:
            Database.return_connection(conn)

    @staticmethod
    def obtener_por_cliente(cliente_id):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM reserva WHERE cliente_id = %s", (cliente_id,))
                rows = cur.fetchall()
                return [Reserva(*row) for row in rows]
        finally:
            Database.return_connection(conn)

    @staticmethod
    def obtener_por_id(reserva_id):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM reserva WHERE id = %s", (reserva_id,))
                row = cur.fetchone()
                if row:
                    return Reserva(*row)
                return None
        finally:
            Database.return_connection(conn)

    @staticmethod
    def actualizar(reserva_id, fecha_ingreso=None, fecha_salida=None):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                campos = []
                valores = []
                if fecha_ingreso:
                    campos.append("fecha_ingreso = %s")
                    valores.append(fecha_ingreso)
                if fecha_salida:
                    campos.append("fecha_salida = %s")
                    valores.append(fecha_salida)
                valores.append(reserva_id)

                set_clause = ", ".join(campos)
                query = f"UPDATE reserva SET {set_clause} WHERE id = %s"
                cur.execute(query, tuple(valores))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            Database.return_connection(conn)

    @staticmethod
    def eliminar(reserva_id):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM reserva WHERE id = %s", (reserva_id,))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            Database.return_connection(conn)
