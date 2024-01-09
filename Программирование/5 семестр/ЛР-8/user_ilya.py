from app_lr8.models import User

class UserIlya(User):
    def get_data(self):
        return {
            'date_of_birth': 'Not Defined',
            'favorite_movies': ['Not Defined', 'Not Defined', 'Not Defined'],
            'favorite_hobbies': ['Not Defined', 'Not Defined', 'Not Defined']
        }
