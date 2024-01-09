from flask import request, jsonify
from app_lr8.models import User

class StoreUserController:
    def store_user(self):
        user_data = request.json
        user = User(user_data['first_name'], user_data['second_name'], user_data['fathers_name'])
        return jsonify(user.get_data()), 200
