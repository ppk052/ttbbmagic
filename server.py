"""import websockets
import asyncio
import time

class server:
    connected = False
    def __init__(self,message,status):
        self.message = message  
        self.status = False    
        start_server = websockets.serve(self.hello, "localhost", 8000)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever() 
        
    def send(self,cor):
        self.message= cor
        self.status

    async def hello(self,websocket, path):
        name = await websocket.recv()
        print("connected")
        server.connected = True
        print(f"{name}")
        await websocket.send(f"({self.message[0]},{self.message[1]},{self.message[2]})")
        print(f"({self.message[0]},{self.message[1]},{self.message[2]})")
        while True:
            if self.status:
                await websocket.send(f"({self.message[0]},{self.message[1]},{self.message[2]})")
                self.status = False
                print(f"({self.message[0]},{self.message[1]},{self.message[2]})sended")
            #print("("+str(self.message[0])+","+str(self.message[1])+","+str(self.message[2]),")")

    #async def go(self):
        

server1 = server([0,0,0],False)
#server1.go()
print("go ok")
while not server.connected:
    pass
    print(server.connected)
for i in range(5):
    server1.send([1,i*100,250])
    time.sleep(1)
    print(i)"""


"""import asyncio
import websockets

connected_clients = set()

async def handler(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            # Echo the received message back to the client
            await websocket.send(message)
    except websockets.ConnectionClosed:
        print("Connection closed")
    finally:
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "localhost", 8000):
        await asyncio.Future()  # run forever

# Run the server
asyncio.run(main())"""


"""import asyncio
import websockets

connected_clients = set()

async def handler(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            # Echo the received message back to the client
            await websocket.send(message)
    except websockets.ConnectionClosed:
        print("Connection closed")
    finally:
        connected_clients.remove(websocket)

async def send_message_to_clients():
    while True:
        message = input("Enter message to send to all clients: ")
        if connected_clients:  # Check if there are connected clients
            await asyncio.gather(*(client.send(message) for client in connected_clients))

async def main():
    server = await websockets.serve(handler, "localhost", 8000)
    await asyncio.gather(server.wait_closed(), send_message_to_clients())

# Run the server
asyncio.run(main())"""

"""import asyncio
import websockets

connected_clients = set()

async def handler(websocket, path):
    # 클라이언트 연결 시 메시지 출력
    print("Client connected")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            # Echo the received message back to the client
            await websocket.send(message)
    except websockets.ConnectionClosed:
        print("Connection closed")
    finally:
        connected_clients.remove(websocket)
        # 클라이언트 연결 종료 시 메시지 출력
        print("Client disconnected")

async def send_message_to_clients():
    while True:
        message = await asyncio.get_event_loop().run_in_executor(None, input, "Enter message to send to all clients: ")
        if connected_clients:  # Check if there are connected clients
            await asyncio.gather(*(client.send(message) for client in connected_clients))

async def main():
    server = await websockets.serve(handler, "localhost", 8000)
    print("WebSocket server started on ws://localhost:8000")
    await asyncio.gather(server.wait_closed(), send_message_to_clients())

# Run the server
asyncio.run(main())"""
import asyncio
import websockets

class WebSocketServer:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.connected_clients = set()

    async def handler(self, websocket, path):
        print("Client connected")
        self.connected_clients.add(websocket)
        try:
            async for message in websocket:
                print(f"Received message: {message}")
                await websocket.send(message)
        except websockets.ConnectionClosed:
            print("Connection closed")
        finally:
            self.connected_clients.remove(websocket)
            print("Client disconnected")

    async def send_message_to_clients(self):
        while True:
            message = await asyncio.get_event_loop().run_in_executor(None, input, "Enter message to send to all clients: ")
            if self.connected_clients:
                await asyncio.gather(*(client.send(message) for client in self.connected_clients))

    async def start(self):
        server = await websockets.serve(self.handler, self.host, self.port)
        print(f"WebSocket server started on ws://{self.host}:{self.port}")
        await asyncio.gather(server.wait_closed(), self.send_message_to_clients())



