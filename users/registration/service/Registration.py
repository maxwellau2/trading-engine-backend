from typing import List
from users.model.UserModel import UserDB
from keycove import hash
from peewee import Query


class Registration:
    def __init__(self) -> None:
        pass

    def create_table(self):
        UserDB.create_table(safe=False)

    def find_user_by_name(self, username:str) -> List[UserDB]:
        return list(UserDB.select().where(UserDB.username == username))

    def __user_exists__(self, username: str) -> bool:
        result = self.find_user_by_name(username)
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
        res = UserDB.create(username=username, password=hash(password))
        return res.__dict__["__data__"]

    def change_password(self, username: str, new_password: str):
        if not self.__user_exists__(username):
            return None
        query: Query = UserDB.update(password=hash(new_password)).where(
            UserDB.username == username
        )
        result = query.execute()
        return result

    def delete_user(self, username: str, password:str) -> int | None:
        """
        returns None if user DNE
        returns 1 is user is deleted
        """
        if not self.__user_exists__(username):
            return None
        user = self.find_user_by_name(username)
        if user[0].password == hash(password):
            query: Query = UserDB.delete().where(UserDB.username == username)
            res = query.execute()
            return res
        return None
