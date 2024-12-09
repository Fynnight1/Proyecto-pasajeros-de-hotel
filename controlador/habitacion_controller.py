# controlador/habitacion_controller.py

from modelo.habitacion import Habitacion

class HabitacionController:
    def crear_habitacion(self, numero, piso, estado, hotel_id):
        return Habitacion.create(numero, piso, estado, hotel_id)

    def obtener_habitaciones(self):
        return Habitacion.get_all()

    def obtener_habitacion_por_id(self, habitacion_id):
        return Habitacion.get_by_id(habitacion_id)
    
    def obtener_habitaciones_disponibles(self):
        return Habitacion.get_available()

    def actualizar_habitacion(self, habitacion_id, numero=None, piso=None, estado=None, hotel_id=None):
        return Habitacion.update(habitacion_id, numero=numero, piso=piso, estado=estado, hotel_id=hotel_id)

    def eliminar_habitacion(self, habitacion_id):
        return Habitacion.delete(habitacion_id)
    
    def obtener_habitaciones_por_hotel(self, hotel_id):
        return Habitacion.get_by_hotel_id(hotel_id)
