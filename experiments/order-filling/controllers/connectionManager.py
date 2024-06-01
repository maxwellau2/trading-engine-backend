from fastapi import WebSocket
from fastapi.websockets import WebSocketState

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.whitelist = ["abc", "123"]

    def authenticate_token(self, token: str):
        return token in self.whitelist

    async def add_connect(self, websocket: WebSocket):
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            await websocket.close()

    async def send_personal_message(self, message: str, websocket: WebSocket):
        if websocket.application_state == WebSocketState.CONNECTED:
            await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            if connection.application_state == WebSocketState.CONNECTED:
                await connection.send_text(message)