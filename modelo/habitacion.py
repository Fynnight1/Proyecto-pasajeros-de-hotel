# modelo/habitacion.py

from .database import Database

class Habitacion:
    def __init__(self, id, numero, piso, estado, hotel_id):
        self.id = id
        self.numero = numero
        self.piso = piso
        self.estado = estado
        self.hotel_id = hotel_id

    @staticmethod
    def crear(numero, piso, estado, hotel_id):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO habitacion (numero, piso, estado, hotel_id)
                    VALUES (%s, %s, %s, %s) RETURNING id
                """, (numero, piso, estado, hotel_id))
                habitacion_id = cur.fetchone()[0]
                conn.commit()
                return Habitacion(habitacion_id, numero, piso, estado, hotel_id)
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
                cur.execute("SELECT * FROM habitacion")
                rows = cur.fetchall()
                return [Habitacion(*row) for row in rows]
        finally:
            Database.return_connection(conn)

    @staticmethod
    def obtener_por_id(habitacion_id):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM habitacion WHERE id = %s", (habitacion_id,))
                row = cur.fetchone()
                if row:
                    return Habitacion(*row)
                return None
        finally:
            Database.return_connection(conn)

    @staticmethod
    def obtener_por_hotel_id(hotel_id):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM habitacion WHERE hotel_id = %s", (hotel_id,))
                rows = cur.fetchall()
                return [Habitacion(*row) for row in rows]
        finally:
            Database.return_connection(conn)

    @staticmethod
    def obtener_disponibles():
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM habitacion WHERE estado = 'Disponible'")
                rows = cur.fetchall()
                return [Habitacion(*row) for row in rows]
        finally:
            Database.return_connection(conn)

    @staticmethod
    def actualizar(habitacion_id, numero=None, piso=None, estado=None, hotel_id=None):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                campos = []
                valores = []
                if numero:
                    campos.append("numero = %s")
                    valores.append(numero)
                if piso is not None:
                    campos.append("piso = %s")
                    valores.append(piso)
                if estado:
                    campos.append("estado = %s")
                    valores.append(estado)
                if hotel_id:
                    campos.append("hotel_id = %s")
                    valores.append(hotel_id)
                valores.append(habitacion_id)

                set_clause = ", ".join(campos)
                query = f"UPDATE habitacion SET {set_clause} WHERE id = %s"
                cur.execute(query, tuple(valores))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            Database.return_connection(conn)

    @staticmethod
    def eliminar(habitacion_id):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM habitacion WHERE id = %s", (habitacion_id,))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            Database.return_connection(conn)
