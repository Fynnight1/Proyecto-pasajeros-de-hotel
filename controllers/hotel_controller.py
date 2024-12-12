# controllers/hotel_controller.py

from models.hotel import Hotel

class HotelController:
    def create_hotel(self, name, address, phone):
        return Hotel.create(name, address, phone)

    def get_hotels(self):
        return Hotel.get_all()

    def get_hotel_by_id(self, hotel_id):
        return Hotel.get_by_id(hotel_id)

    def update_hotel(self, hotel_id, name=None, address=None, phone=None):
        return Hotel.update(hotel_id, name, address, phone)

    def delete_hotel(self, hotel_id):
        return Hotel.delete(hotel_id)
