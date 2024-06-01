import asyncio
from websockets.server import serve

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)
        print(message)

async def send_nudes(websocket):
    async for message in websocket:
        await websocket.send("nudes sent")
        print(message)

async def main():
    async with serve(send_nudes, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())