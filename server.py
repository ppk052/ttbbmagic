"""from picamera2 import Picamera2, Preview"""
import websockets
import asyncio
import time
import tracking.facialtracking as facialTracking
import tracking.tracking as tracking

class server:
    connected = False
    def __init__(self,message,status):
        self.message = message  
        self.status = False    
        start_server = websockets.serve(self.hello, "localhost", 8000)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever() 

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
    async def sendcor(self,websocket, traking ,update):
        while True:
            if update:
                await websocket.send(f"()")

    #async def go(self):
        

server1 = server([1,0,0],False)
#server1.go()
print("go ok")
tracking1 = tracking()
while not server.connected:
    pass
    print(server.connected)

tracking1.runTracking()
while True:
    if tracking1.update:
        server1.message = f"(1, {tracking1.getsunpos()[0]},{tracking1.sunpos[1]})"
        server1.status = True
        tracking1.confirm()
    """
    facialTracking.runFacialTrakcing(num)
    num+=1
    if num == 2:
        num = 0"""
