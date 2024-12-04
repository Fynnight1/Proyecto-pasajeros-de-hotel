from modelo.conexion import obtener_conexion

class AdministradorController:
    def _init_(self):
        print("AdministradorController._init_ llamado")
        self.conexion = obtener_conexion()
        if self.conexion is None:
            print("No se pudo establecer la conexión a la base de datos.")

    def autenticar(self, username, password):
        print("AdministradorController.autenticar llamado")
        if self.conexion is None:
            print("Conexión a la base de datos no establecida.")
            return False
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("""
                    SELECT id FROM public.administrador
                    WHERE username=%s AND password=%s
                """, (username, password))
                resultado = cursor.fetchone()
                return resultado is not None
        except Exception as e:
            print("Error al autenticar:", e)
            return False