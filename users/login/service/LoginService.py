from typing import List
from users.model.UserModel import UserDB
import jwt
import os
from dotenv import load_dotenv
from keycove import hash
from datetime import datetime, timedelta

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")

class LoginService:
    def login(username:str, password_unhashed:str) -> str|None:
        """
        returns the jwt token if successful, else returns null on failure
        """
        result: List[UserDB] = list(UserDB.select().where(UserDB.username == username and UserDB.password == hash(password_unhashed)))
        if len(result) != 0:
            # return jwt token with credentials here
            encoded_jwt = jwt.encode({"id": str(result[0].id),
                                    "username": result[0].username,
                                    "expiration":  int((datetime.now() + timedelta(hours=1)).timestamp())
                                    }, JWT_SECRET, algorithm="HS256")
            return encoded_jwt
        return None

