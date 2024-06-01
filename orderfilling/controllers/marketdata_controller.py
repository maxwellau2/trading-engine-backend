from fastapi import APIRouter
from orderfilling.currency import currency

router = APIRouter(prefix="/api", tags=["gayyy"])

@router.get("/users")
async def read_users():
    return [{"name" : "Jonathan Tan"}, {"name": "poopooman"}]

@router.post("/fill_order/{coins}")
async def fill_order(coins: float):
    currency.fill_order(coins)
    return {"message": "Order filled", "state": currency.get_state()}