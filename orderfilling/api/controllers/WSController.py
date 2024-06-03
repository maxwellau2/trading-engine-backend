import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from fastapi import APIRouter
from ..utils.ConnectionManager import ConnectionManager
from orderfilling.orderbook.OrderbookPool import OrderBookPool

router = APIRouter(prefix="/ws")
manager = ConnectionManager()
pool = OrderBookPool()

@router.websocket("/livedata/{client_id}/{ticker}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, ticker:str):
    print(manager.active_connections)
    await websocket.accept()
    # authenticate websocket client ID, in manager.whitelist
    # check if client id is in whitelist
    if not manager.authenticate_token(client_id):
        await websocket.send_text("invalid, sorry")
        await websocket.close()
        # await websocket.send_denial_response(response) to be used
        return
    # check orderbook pool
    book = pool.get_order_book_by_name(ticker)
    if not book:
        await websocket.send_text("invalid ticker")
        await websocket.close()
        return

    # passed the vibe check
    await manager.add_connect(websocket)
    try:
        while True:
            state = book.get_market_state()
            await manager.send_personal_message(f"{state.__dict__}", websocket)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        # no need to disconnect, just remove
        print(f"Client disconnected: {client_id}")
        manager.remove_from_active(websocket)
    except Exception as e:
        # fucker tryna play punk lol
        print(f"Error: {e}")
        await manager.disconnect(websocket)
