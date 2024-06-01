import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from fastapi import APIRouter
from currency import currency
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
        return
    # client id is in whitelist
    await manager.add_connect(websocket)
    try:
        while True:
            state = currency.get_state()
            await manager.broadcast(f"{state}") # broadcast to all 
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except Exception as e:
        print(e)
