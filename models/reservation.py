# models/reservation.py

from .database import Database

class Reservation:
    def __init__(self, id, client_id, room_id, worker_id, check_in_date, check_out_date):
        self.id = id
        self.client_id = client_id
        self.room_id = room_id
        self.worker_id = worker_id
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date

    @staticmethod
    def create(client_id, room_id, worker_id, check_in_date, check_out_date):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO reservation (client_id, room_id, worker_id, check_in_date, check_out_date)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id
                """, (client_id, room_id, worker_id, check_in_date, check_out_date))
                reservation_id = cur.fetchone()[0]
                conn.commit()
                return Reservation(reservation_id, client_id, room_id, worker_id, check_in_date, check_out_date)
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
                cur.execute("SELECT * FROM reservation")
                rows = cur.fetchall()
                return [Reservation(*row) for row in rows]
        finally:
            Database.return_connection(conn)

    @staticmethod
    def get_by_client(client_id):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM reservation WHERE client_id = %s", (client_id,))
                rows = cur.fetchall()
                return [Reservation(*row) for row in rows]
        finally:
            Database.return_connection(conn)

    @staticmethod
    def get_by_id(reservation_id):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM reservation WHERE id = %s", (reservation_id,))
                row = cur.fetchone()
                if row:
                    return Reservation(*row)
                return None
        finally:
            Database.return_connection(conn)

    @staticmethod
    def update(reservation_id, check_in_date=None, check_out_date=None):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                fields = []
                values = []
                if check_in_date:
                    fields.append("check_in_date = %s")
                    values.append(check_in_date)
                if check_out_date:
                    fields.append("check_out_date = %s")
                    values.append(check_out_date)
                values.append(reservation_id)

                set_clause = ", ".join(fields)
                query = f"UPDATE reservation SET {set_clause} WHERE id = %s"
                cur.execute(query, tuple(values))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            Database.return_connection(conn)

    @staticmethod
    def delete(reservation_id):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM reservation WHERE id = %s", (reservation_id,))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            Database.return_connection(conn)
