# controllers/user_controller.py

from models.user import User

class UserController:
    def create_user(self, name, rut, address, phone, username, password, role):
        return User.create(name, rut, address, phone, username, password, role)

    def authenticate(self, username, password):
        return User.authenticate(username, password)

    def get_users(self):
        return User.get_all()

    def get_user_by_id(self, user_id):
        return User.get_by_id(user_id)

    def update_user(self, user_id, name=None, rut=None, address=None, phone=None, username=None, password=None, role=None, active=None):
        return User.update(user_id, name, rut, address, phone, username, password, role, active)

    def deactivate_user(self, user_id):
        return User.deactivate(user_id)
