from fastapi import APIRouter
from users.registration.controller import RegistrationController

router = APIRouter(prefix="/users")

router.include_router(RegistrationController.router)
