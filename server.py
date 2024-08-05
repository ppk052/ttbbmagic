import websockets
import asyncio

class server:

    status = False
    message = [0,0,0]

    async def send(cor):
        global message 
        message= cor
        global status 
        status= True

    async def hello(websocket, path):
        global message
        global status
        name = await websocket.recv()
        print("connected")
        print(f"{name}")
        #await websocket.send("(1,250,300)")
        while True:
            if status:
                await websocket.send(str(message))
                status = False
                print(f"{str(message)}sended")

    start_server = websockets.serve(hello, "localhost", 8000)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()