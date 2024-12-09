# controlador/reserva_controller.py

from modelo.reserva import Reserva

class ReservaController:
    def crear_reserva(self, cliente_id, habitacion_id, trabajador_id, fecha_ingreso, fecha_salida):
        return Reserva.create(cliente_id, habitacion_id, trabajador_id, fecha_ingreso, fecha_salida)

    def obtener_reservas(self):
        return Reserva.get_all()

    def obtener_reservas_por_cliente(self, cliente_id):
        return Reserva.get_by_cliente(cliente_id)
    
    def obtener_reserva_por_id(self, reserva_id):
        return Reserva.get_by_id(reserva_id)  # Asegúrate de implementar este método en el modelo Reserva

    def actualizar_reserva(self, reserva_id, fecha_ingreso=None, fecha_salida=None):
        return Reserva.update(reserva_id, fecha_ingreso=fecha_ingreso, fecha_salida=fecha_salida)
    
    def eliminar_reserva(self, reserva_id):
        return Reserva.delete(reserva_id)
