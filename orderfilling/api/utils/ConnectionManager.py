from fastapi import WebSocket
from fastapi.websockets import WebSocketState


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.whitelist = ["abc", "123"]

    def authenticate_token(self, token: str) -> bool:
        return token in self.whitelist

    async def add_connect(self, websocket: WebSocket):
        self.active_connections.append(websocket)
        print(f"Connected: {websocket.client}")
        print(f"Active connections: {len(self.active_connections)}")

    def remove_from_active(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            if websocket.client_state != WebSocketState.DISCONNECTED:
                await websocket.close()
            self.remove_from_active(websocket)
            print(f"Disconnected: {websocket.client}")
        else:
            print(f"WebSocket not found in active connections: {websocket.client}")
        print(f"Active connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        if websocket.client_state == WebSocketState.CONNECTED:
            try:
                await websocket.send_text(message)
            except RuntimeError:
                print(
                    f"Attempted to send message to a closed WebSocket: {websocket.client}"
                )

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            if connection.client_state == WebSocketState.CONNECTED:
                await self.send_personal_message(message, connection)
