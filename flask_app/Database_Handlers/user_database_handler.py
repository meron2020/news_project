from flask_app.Models.usermodel import UserModel


class UserDatabaseHandler:
    def save_user_to_db(self, user):
        user.save_to_db()

    @classmethod
    def get_by_username(cls, username):
        return UserModel.find_by_username(username)

    @classmethod
    def get_by_id(cls, user_id):
        return UserModel.find_by_id(user_id)

    def delete_from_db(self, user):
        user.delete_to_db()
