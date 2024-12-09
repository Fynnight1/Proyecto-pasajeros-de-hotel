# modelo/usuario.py

from .database import Database
import bcrypt

class Usuario:
    def __init__(self, id, nombre, rut, direccion, telefono, username, password, rol, activo):
        self.id = id
        self.nombre = nombre
        self.rut = rut
        self.direccion = direccion
        self.telefono = telefono
        self.username = username
        self.password = password
        self.rol = rol
        self.activo = activo

    @staticmethod
    def crear(nombre, rut, direccion, telefono, username, password, rol):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO usuario (nombre, rut, direccion, telefono, username, password, rol)
                    VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
                """, (nombre, rut, direccion, telefono, username, hashed_password, rol))
                usuario_id = cur.fetchone()[0]
                conn.commit()
                return Usuario(usuario_id, nombre, rut, direccion, telefono, username, hashed_password, rol, True)
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            Database.return_connection(conn)

    @staticmethod
    def autenticar(username, password):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM usuario WHERE username = %s AND activo = TRUE", (username,))
                row = cur.fetchone()
                if row and bcrypt.checkpw(password.encode('utf-8'), row[6].encode('utf-8')):
                    return Usuario(*row)
                return None
        finally:
            Database.return_connection(conn)

    @staticmethod
    def obtener_todos():
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM usuario")
                rows = cur.fetchall()
                return [Usuario(*row) for row in rows]
        finally:
            Database.return_connection(conn)

    @staticmethod
    def obtener_por_id(usuario_id):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM usuario WHERE id = %s", (usuario_id,))
                row = cur.fetchone()
                if row:
                    return Usuario(*row)
                return None
        finally:
            Database.return_connection(conn)

    @staticmethod
    def actualizar(usuario_id, nombre, rut, direccion, telefono, username, password, rol, activo):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                campos = []
                valores = []
                if nombre:
                    campos.append("nombre = %s")
                    valores.append(nombre)
                if rut:
                    campos.append("rut = %s")
                    valores.append(rut)
                if direccion:
                    campos.append("direccion = %s")
                    valores.append(direccion)
                if telefono:
                    campos.append("telefono = %s")
                    valores.append(telefono)
                if username:
                    campos.append("username = %s")
                    valores.append(username)
                if password:
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    campos.append("password = %s")
                    valores.append(hashed_password)
                if rol:
                    campos.append("rol = %s")
                    valores.append(rol)
                if activo is not None:
                    campos.append("activo = %s")
                    valores.append(activo)
                valores.append(usuario_id)

                set_clause = ", ".join(campos)
                query = f"UPDATE usuario SET {set_clause} WHERE id = %s"
                cur.execute(query, tuple(valores))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            Database.return_connection(conn)

    @staticmethod
    def desactivar(usuario_id):
        conn = Database.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("UPDATE usuario SET activo = FALSE WHERE id = %s", (usuario_id,))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            Database.return_connection(conn)
