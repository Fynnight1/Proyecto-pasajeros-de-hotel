import psycopg2

def obtener_conexion():
    try:
        conexion = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="Fynnight",
            options='-c search_path=public'
        )
        return conexion
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None