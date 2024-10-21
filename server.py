"""from picamera2 import Picamera2, Preview"""
import websockets
import asyncio
import time
#import tracking.facialtracking as facialTracking
import eyePos3D
import sunPos3D
import trackingcam

class server(trackingcam.trackingcam):
    connected = False
    def __init__(self,message,status):
        super().__init__()
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
            self.runTracking()
            if self.update:
                if self.bright <= 10:
                    server1.message = [0,self.getsunpos()[0],self.sunpos[1]]
                else:
                    self.calculatedleft = eyePos3D.runEyePos3D(self.eyeposcam1[0][0],self.eyeposcam1[0][1],self.tracking1.eyeposcam2[0][0],self.tracking1.eyeposcam2[0][1])
                    self.calculatedright = eyePos3D.runEyePos3D(self.eyeposcam1[1][0],self.eyeposcam1[1][1],self.tracking1.eyeposcam2[1][0],self.tracking1.eyeposcam2[1][1])            
                    server1.message = [1,self.calculatedleft[0],self.calculatedleft[1]]
                server1.status = True
                self.confirm()
            if self.status:
                await websocket.send(f"({self.message[0]},{self.message[1]},{self.message[2]})")
                self.status = False
                print(f"({self.message[0]},{self.message[1]},{self.message[2]})sended")
            #print("("+str(self.message[0])+","+str(self.message[1])+","+str(self.message[2]),")")
    """async def sendcor(self,websocket, traking ,update):
        while True:
            if update:
                await websocket.send(f"()")"""

    #async def go(self):
        

server1 = server([0,0,0],False)
#server1.go()
"""
print("go ok")
tracking1 = trackingcam.tracking()
while not server.connected:
    pass
    print(server.connected)

while True:
    tracking1.runTracking()
    if tracking1.update:
        if tracking1.bright <= 10:
            server1.message = [0,tracking1.getsunpos()[0],tracking1.sunpos[1]]
        else:
            calculatedleft = eyePos3D.runEyePos3D(tracking1.eyeposcam1[0][0],tracking1.eyeposcam1[0][1],tracking1.eyeposcam2[0][0],tracking1.eyeposcam2[0][1])
            calculatedright = eyePos3D.runEyePos3D(tracking1.eyeposcam1[1][0],tracking1.eyeposcam1[1][1],tracking1.eyeposcam2[1][0],tracking1.eyeposcam2[1][1])            
            server1.message = [1,calculatedleft[0],calculatedleft[1]]
        server1.status = True
        tracking1.confirm()
"""