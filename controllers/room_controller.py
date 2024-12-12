# controllers/room_controller.py

from models.room import Room

class RoomController:
    def create_room(self, number, floor, status, hotel_id):
        return Room.create(number, floor, status, hotel_id)

    def get_rooms(self):
        return Room.get_all()

    def get_room_by_id(self, room_id):
        return Room.get_by_id(room_id)
    
    def get_available_rooms(self):
        return Room.get_available()
    
    def update_room(self, room_id, number=None, floor=None, status=None, hotel_id=None):
        return Room.update(room_id, number=number, floor=floor, status=status, hotel_id=hotel_id)

    def delete_room(self, room_id):
        return Room.delete(room_id)
    
    def get_rooms_by_hotel(self, hotel_id):
        return Room.get_by_hotel_id(hotel_id)
