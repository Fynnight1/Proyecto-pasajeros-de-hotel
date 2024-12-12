# models/hotel.py
from .database import Database

class Hotel:
    def __init__(self, id, name, address, phone):
        self.id = id
        self.name = name
        self.address = address
        self.phone = phone

    @staticmethod
    def create(name, address, phone):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO hotel (name, address, phone)
                    VALUES (%s, %s, %s) RETURNING id
                """, (name, address, phone))
                hotel_id = cur.fetchone()[0]
                conn.commit()
                return Hotel(hotel_id, name, address, phone)
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            Database.return_connection(conn)

    @staticmethod
    def get_all():
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, address, phone FROM hotel")
                rows = cur.fetchall()
                return [Hotel(*row) for row in rows]
        finally:
            Database.return_connection(conn)

    @staticmethod
    def get_by_id(hotel_id):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, address, phone FROM hotel WHERE id = %s", (hotel_id,))
                row = cur.fetchone()
                if row:
                    return Hotel(*row)
                return None
        finally:
            Database.return_connection(conn)

    @staticmethod
    def update(hotel_id, name=None, address=None, phone=None):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                fields = []
                values = []
                if name:
                    fields.append("name = %s")
                    values.append(name)
                if address:
                    fields.append("address = %s")
                    values.append(address)
                if phone:
                    fields.append("phone = %s")
                    values.append(phone)
                if not fields:
                    return False
                values.append(hotel_id)
                set_clause = ", ".join(fields)
                query = f"UPDATE hotel SET {set_clause} WHERE id = %s"
                cur.execute(query, tuple(values))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            Database.return_connection(conn)

    @staticmethod
    def delete(hotel_id):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM hotel WHERE id = %s", (hotel_id,))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            Database.return_connection(conn)
