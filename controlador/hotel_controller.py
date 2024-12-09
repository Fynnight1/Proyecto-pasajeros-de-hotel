# controlador/hotel_controller.py

from modelo.hotel import Hotel

class HotelController:
    def crear_hotel(self, nombre, direccion, telefono):
        return Hotel.create(nombre, direccion, telefono)

    def obtener_hoteles(self):
        return Hotel.get_all()

    def obtener_hotel_por_id(self, hotel_id):
        return Hotel.get_by_id(hotel_id)
    
    def actualizar_hotel(self, hotel_id, nombre=None, direccion=None, telefono=None):
        return Hotel.update(hotel_id, nombre=nombre, direccion=direccion, telefono=telefono)

    def eliminar_hotel(self, hotel_id):
        return Hotel.delete(hotel_id)
