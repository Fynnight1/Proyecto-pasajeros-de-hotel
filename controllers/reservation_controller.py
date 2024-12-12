# controllers/reservation_controller.py

from models.reservation import Reservation

class ReservationController:
    def create_reservation(self, client_id, room_id, worker_id, check_in_date, check_out_date):
        return Reservation.create(client_id, room_id, worker_id, check_in_date, check_out_date)

    def get_reservations(self):
        return Reservation.get_all()

    def get_reservations_by_client(self, client_id):
        return Reservation.get_by_client(client_id)
    
    def get_reservation_by_id(self, reservation_id):
        return Reservation.get_by_id(reservation_id)  # Ensure this method is implemented in the Reservation model

    def update_reservation(self, reservation_id, check_in_date=None, check_out_date=None):
        return Reservation.update(reservation_id, check_in_date=check_in_date, check_out_date=check_out_date)
    
    def delete_reservation(self, reservation_id):
        return Reservation.delete(reservation_id)
