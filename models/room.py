# models/room.py

from .database import Database

class Room:
    def __init__(self, id, number, floor, status, hotel_id):
        self.id = id
        self.number = number
        self.floor = floor
        self.status = status
        self.hotel_id = hotel_id

    @staticmethod
    def create(number, floor, status, hotel_id):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO room (number, floor, status, hotel_id)
                    VALUES (%s, %s, %s, %s) RETURNING id
                """, (number, floor, status, hotel_id))
                room_id = cur.fetchone()[0]
                conn.commit()
                return Room(room_id, number, floor, status, hotel_id)
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
                cur.execute("SELECT * FROM room")
                rows = cur.fetchall()
                return [Room(*row) for row in rows]
        finally:
            Database.return_connection(conn)

    @staticmethod
    def get_by_id(room_id):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM room WHERE id = %s", (room_id,))
                row = cur.fetchone()
                if row:
                    return Room(*row)
                return None
        finally:
            Database.return_connection(conn)

    @staticmethod
    def get_by_hotel_id(hotel_id):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM room WHERE hotel_id = %s", (hotel_id,))
                rows = cur.fetchall()
                return [Room(*row) for row in rows]
        finally:
            Database.return_connection(conn)

    @staticmethod
    def get_available():
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM room WHERE status = 'Available'")
                rows = cur.fetchall()
                return [Room(*row) for row in rows]
        finally:
            Database.return_connection(conn)

    @staticmethod
    def update(room_id, number=None, floor=None, status=None, hotel_id=None):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                fields = []
                values = []
                if number:
                    fields.append("number = %s")
                    values.append(number)
                if floor is not None:
                    fields.append("floor = %s")
                    values.append(floor)
                if status:
                    fields.append("status = %s")
                    values.append(status)
                if hotel_id:
                    fields.append("hotel_id = %s")
                    values.append(hotel_id)
                values.append(room_id)

                set_clause = ", ".join(fields)
                query = f"UPDATE room SET {set_clause} WHERE id = %s"
                cur.execute(query, tuple(values))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            Database.return_connection(conn)

    @staticmethod
    def delete(room_id):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM room WHERE id = %s", (room_id,))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            Database.return_connection(conn)
