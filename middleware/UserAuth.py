from typing import List
import jwt
import os
from dotenv import load_dotenv
from users.model.UserModel import UserDB

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")

class UserAuth:
    def check_jwt(jwt_token: str):
        # decode the jwt
        result = jwt.decode(jwt=jwt_token, key=JWT_SECRET,algorithms=["HS256"])
        # check the jwt template
        if "id" not in result:
            return False
        if "username" not in result:
            return False
        if "expiration" not in result:
            return False
        # check if id and username are congruent
        result: List[UserDB] = list(UserDB.select().where(UserDB.username == result["username"] and UserDB.id == result["id"]))
        print(result[0].username, result[0].id)
        if len(result) != 0:
            return True
        

