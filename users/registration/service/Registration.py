from users.registration.model.UserModel import UserDB
from keycove import generate_token, hash, encrypt, generate_secret_key
from peewee import PostgresqlDatabase


class Registration:
    def __init__(self, db_connection: PostgresqlDatabase) -> None:
        self.users = UserDB()

    def __user_exists__(self, username: str) -> bool:
        result = list(self.users.select().where(UserDB.username == username))
        if len(result) != 0:
            return True
        return False

    def verify(self, api_key: str, secret_key: str):
        pass

    # to use, api key management
    # api_key = generate_token()
    # new_user.api_key_hash = hash(api_key)

    # secret_key = generate_secret_key()
    # new_user.api_secret_hash = hash(secret_key)

    def create_user(self, username: str, password: str) -> dict | None:
        if self.__user_exists__(username):
            return None
        new_user = UserDB()
        new_user.username = username
        new_user.password = hash(password)

        new_user.save()
        return new_user.__dict__["__data__"]

    def change_password(self, username: str, new_password: str):
        if not self.__user_exists__(username):
            return None
        user = UserDB()
        query = UserDB.update(password=new_password).where(user.username == username)
        query.execute()

    def delete_user(self, username: str):
        if not self.__user_exists__(username):
            return None
        user = UserDB()
        query = user.delete().where()
