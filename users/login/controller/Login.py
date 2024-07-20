from fastapi import APIRouter,Response
from users.login.service.LoginService import LoginService
import json

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/userlogin")
async def login(username:str, password:str):
    print()
    token = LoginService.login(username = username, password_unhashed = password)
    print(token)
    if token:
        response = json.dumps({"message": "success", "token": token})
        resp =  Response(content= response, status_code=200)
        resp.set_cookie("payload", token, httponly=True, secure=True)
        return resp
    else:
        response = json.dumps({"message": "invalid credentials", "token": ""})
        resp = Response(content=response, status_code=400)
        resp.delete_cookie("payload")
        return resp