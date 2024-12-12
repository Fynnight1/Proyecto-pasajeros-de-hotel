# models/user.py

from .database import Database
import bcrypt  # type: ignore

class User:
    def __init__(self, id, name, rut, address, phone, username, password, role, active):
        self.id = id
        self.name = name
        self.rut = rut
        self.address = address
        self.phone = phone
        self.username = username
        self.password = password
        self.role = role
        self.active = active

    @staticmethod
    def create(name, rut, address, phone, username, password, role):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO "user" (name, rut, address, phone, username, password, role)
                    VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
                """, (name, rut, address, phone, username, hashed_password, role))
                user_id = cur.fetchone()[0]
                conn.commit()
                return User(user_id, name, rut, address, phone, username, hashed_password, role, True)
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            Database.return_connection(conn)

    @staticmethod
    def authenticate(username, password):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "user" WHERE username = %s AND active = TRUE', (username,))
                row = cur.fetchone()
                if row and bcrypt.checkpw(password.encode('utf-8'), row[6].encode('utf-8')):
                    return User(*row)
                return None
        finally:
            Database.return_connection(conn)

    @staticmethod
    def get_all():
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "user"')
                rows = cur.fetchall()
                return [User(*row) for row in rows]
        finally:
            Database.return_connection(conn)

    @staticmethod
    def get_by_id(user_id):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "user" WHERE id = %s', (user_id,))
                row = cur.fetchone()
                if row:
                    return User(*row)
                return None
        finally:
            Database.return_connection(conn)

    @staticmethod
    def update(user_id, name=None, rut=None, address=None, phone=None, username=None, password=None, role=None, active=None):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                fields = []
                values = []
                if name:
                    fields.append("name = %s")
                    values.append(name)
                if rut:
                    fields.append("rut = %s")
                    values.append(rut)
                if address:
                    fields.append("address = %s")
                    values.append(address)
                if phone:
                    fields.append("phone = %s")
                    values.append(phone)
                if username:
                    fields.append("username = %s")
                    values.append(username)
                if password:
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    fields.append("password = %s")
                    values.append(hashed_password)
                if role:
                    fields.append("role = %s")
                    values.append(role)
                if active is not None:
                    fields.append("active = %s")
                    values.append(active)
                values.append(user_id)

                set_clause = ", ".join(fields)
                query = f'UPDATE "user" SET {set_clause} WHERE id = %s'
                cur.execute(query, tuple(values))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            Database.return_connection(conn)

    @staticmethod
    def deactivate(user_id):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute('UPDATE "user" SET active = FALSE WHERE id = %s', (user_id,))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            Database.return_connection(conn)
