class Reserva:
    def _init_(self, id, cliente_id, habitacion_id, trabajador_id, fecha_ingreso, fecha_salida):
        self.id = id
        self.cliente_id = cliente_id
        self.habitacion_id = habitacion_id
        self.trabajador_id = trabajador_id
        self.fecha_ingreso = fecha_ingreso
        self.fecha_salida = fecha_salida