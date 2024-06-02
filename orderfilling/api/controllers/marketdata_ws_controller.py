import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from fastapi import APIRouter
from orderfilling.orderbook.currency_singleton import currency
from .connectionManager import ConnectionManager

router = APIRouter(prefix="/ws")
manager = ConnectionManager()

@router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    print(manager.active_connections)
    await websocket.accept()
    # authenticate websocket client ID, in manager.whitelist
    if not manager.authenticate_token(client_id):
        await websocket.send_text("invalid, sorry")
        await websocket.close()
        # await websocket.send_denial_response(response) to be used
        return
    # client id is in whitelist
    await manager.add_connect(websocket)
    try:
        while True:
            state = currency.get_state()
            await manager.send_personal_message(f"{state}", websocket)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        # no need to disconnect, just remove
        print(f"Client disconnected: {client_id}")
        manager.remove_from_active(websocket)
    except Exception as e:
        # fucker tryna play punk lol
        print(f"Error: {e}")
        await manager.disconnect(websocket)
