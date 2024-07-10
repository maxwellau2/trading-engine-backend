from fastapi import APIRouter, Response
from users.registration.service.Registration import Registration
import json


reg = Registration()
router = APIRouter(prefix="/register", tags=["Registration"])


@router.post("/signup")
async def signup(username: str, password: str, email: str):
    result = reg.create_user(username, password, email)
    if result == None:
        resp = str({"status": "failed", "message": "username exists"})
        return Response(content=resp, status_code=200)
    resp = str(
        {
            "status": "success",
            "message": f"verification email sent! {result['username']}",
        }
    )
    print(resp)
    return Response(content=resp, status_code=200)


@router.delete("/deleteuser")
async def delete_user(username: str, password: str):
    result = reg.delete_user(username, password)
    if result == None:
        resp = str({"status": "failed", "message": "user does not exist"})
        return Response(content=resp, status_code=404)
    resp = str({"status": "success", "message": "user deleted"})
    return Response(content=resp, status_code=200)

@router.post("/verify")
async def verify_user(key: str):
    result = reg.verify_new_user(key)
    print("result", result)
    if not result:
        resp = str({"status": "failed", "message": "invalid verification key"})
        return Response(content=resp, status_code=400)
    resp = str({"status": "success", "message": "user created"})
    return Response(content=resp, status_code=200)