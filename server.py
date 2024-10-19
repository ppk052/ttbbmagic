import websockets
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
        

server1 = server([1,0,0],False)
#server1.go()
print("go ok")
while not server.connected:
    pass
    print(server.connected)
for i in range(5):
    server1.send([1,i*100,250])
    time.sleep(1)
    print(i)
