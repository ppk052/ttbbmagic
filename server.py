import websockets
import asyncio

async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = "(0,100,100)"
    await websocket.send(greeting)
    print(f"> {greeting}")

start_server = websockets.serve(hello, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()