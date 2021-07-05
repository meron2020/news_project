from flask_app.Models.usermodel import UserModel
from flask_app.Database_Handlers.user_database_handler import UserDatabaseHandler


def authenticate(username, password):
    user = UserDatabaseHandler.get_by_username(username)
    if user and user.password == password:
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
