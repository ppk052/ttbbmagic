from picamera2 import Picamera2, Preview
from libcamera import controls
import websockets
import asyncio
import time
import eyePos3D
import sunPos3D_new
import display_new
import mediapipe as mp
import numpy as np
import cv2
import os

class server:
    connected = False
    def __init__(self,message,status):
        self.eyeposcam1 = [[0,0],[0,0]]
        self.eyeposcam2 = [[0,0],[0,0]]
        self.sunpos1 = [0,0]
        self.sunpos2 = [0,0]
        self.num = 0
        self.update = False
        self.bright = 0;
        self.message = message  
        self.status = False    
        self.calculatedleft = [0,0,0]
        self.calculatedright = [0,0,0]
        self.calculatedsun=[0,0,0]
        self.calculateddp=[0,0]
        self.message = message  
        self.status = False
        self.max_eyecnt = 5
        self.max_suncnt = 10
        self.max_not_recg = 5
        #선트래킹을 위한 변수
        self.sun_center = [0,0]
        self.camchange =0
        self.find = True
        self.firstsend = True
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
            mp_face_mesh = mp.solutions.face_mesh
            mp_drawing = mp.solutions.drawing_utils
            
            # 홍채의 랜드마크 인덱스
            LEFT_IRIS = [474, 475, 476, 477]
            RIGHT_IRIS = [469, 470, 471, 472]
            
            #time.sleep(0.4)

            #카메라 초점거리 조절 AfMode-초점모드, libcamera의 controls.AfModeEnum사용, LensPostion-초점거리조절, 원하는 초점거리의 역수로 설정
            #picam0.set_controls({"AfMode":controls.AfModeEnum.Manual, "LensPosition":float(1/self.focus)})
            
            print(f"{self.num}번째 카메라")
            # 0,1 : 동공좌표추출, 2:해좌표추출
            if self.num==0 or self.num == 1:
                # Picamera2 초기화
                picam0=Picamera2(self.num)
                picam0.start()
                cnt = 0
                no_cnt = 0
                #눈위치 초기화
                if self.num == 0: self.eyeposcam1 = [[0,0],[0,0]]
                elif self.num == 1: self.eyeposcam2 = [[0,0],[0,0]]
                with mp_face_mesh.FaceMesh(
                    max_num_faces=1,
                    refine_landmarks=True,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as face_mesh:
                    
                    while cnt <= self.max_eyecnt: 
                        # Picamera2에서 이미지를 캡처
                        image = picam0.capture_array()  
                        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # BGR로 변환 (Picamera는 기본적으로 RGB를 반환)
                        # MediaPipe Face Mesh 처리
                        #results는 눈 잡았는지 확인하는 boolean
                        cnt+=1
                        results = face_mesh.process(image)
                        if results.multi_face_landmarks:
                            for face_landmarks in results.multi_face_landmarks:
                                
                                # 왼쪽 홍채
                                left_iris_points = []
                                for idx in LEFT_IRIS:
                                    x = int(face_landmarks.landmark[idx].x * image.shape[1]) - (image.shape[1] / 2)
                                    y = int(face_landmarks.landmark[idx].y * image.shape[0]) - (image.shape[0] / 2)
                                    left_iris_points.append((x, y))
                                left_iris_points = np.array(left_iris_points, dtype=np.int32)
                                (lx, ly), left_radius = cv2.minEnclosingCircle(left_iris_points)
                                left_center = (int(lx) * -1, int(ly) * -1)
                                left_radius = int(left_radius)
                                
                                # 오른쪽 홍채
                                right_iris_points = []
                                for idx in RIGHT_IRIS:
                                    x = int(face_landmarks.landmark[idx].x * image.shape[1]) - (image.shape[1] / 2)
                                    y = int(face_landmarks.landmark[idx].y * image.shape[0]) - (image.shape[0] / 2)
                                    right_iris_points.append((x, y))
                                right_iris_points = np.array(right_iris_points, dtype=np.int32)
                                (rx, ry), right_radius = cv2.minEnclosingCircle(right_iris_points)
                                right_center = (int(rx) * -1, int(ry) * -1)
                                right_radius = int(right_radius)
                                if self.num==0:
                                    for i in range(2):
                                        self.eyeposcam1[0][i] += left_center[i]
                                    for i in range(2):
                                        self.eyeposcam1[1][i] += right_center[i]
                                else:
                                    for i in range(2):
                                        self.eyeposcam2[0][i] += left_center[i]
                                    for i in range(2):
                                        self.eyeposcam2[1][i] += right_center[i]
                        else:
                            no_cnt+=1
                    print("===debug3===")
                    picam0.close()
                #end of while
                #max_num = 50
                if no_cnt == self.max_eyecnt+1:
                    self.num = 0
                    continue
                elif self.num == 0:
                    for i in range(2):
                        self.eyeposcam1[0][i] /= (self.max_eyecnt - no_cnt + 1) 
                    for i in range(2):
                        self.eyeposcam1[1][i] /= (self.max_eyecnt - no_cnt + 1) 
                else:
                    for i in range(2):
                        self.eyeposcam2[0][i] /= (self.max_eyecnt - no_cnt + 1) 
                    for i in range(2):
                        self.eyeposcam2[1][i] /= (self.max_eyecnt - no_cnt + 1) 
                self.num+=1
                print("===debug4===")
            #태양위치추출
            elif self.num==2 or self.num==3:
                cnt = 0
                not_recg = 0
                while cnt <=self.max_suncnt:
                    cnt2 = 0
                    picam0=Picamera2(self.num)
                    picam0.start()
                    while cnt2 < 10:
                        image = picam0.capture_array()  
                        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # BGR로 변환 (Picamera는 기본적으로 RGB를 반환)
                        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        blurred_image = cv2.GaussianBlur(gray, (31, 31), 0)
                        _, threshold_img = cv2.threshold(blurred_image, 252, 255, cv2.THRESH_BINARY)
                        moments = cv2.moments(threshold_img, True)
                        if moments['m00'] != 0:  # Prevent division by zero
                            center_x = int(moments['m10'] / moments['m00'])
                            center_y = int(moments['m01'] / moments['m00'])
                            center = (center_x, center_y)
                            self.set_sun_center(center)
                            print(f"Sun Detected at: {self.sun_center[0]}, {self.sun_center[1]}")
                            self.mod_sun_center(image)
                            if self.num==2:
                                self.sunpos1=self.sun_center
                            else:
                                self.sunpos2=self.sun_center
                                self.update = True
                        else:
                            print("No sun detected.")
                            """if not_recg == self.max_not_recg:
                                await websocket.send("(0,0,0)")
                                self.find = False
                                continue
                            not_recg+=1"""
                        cnt2+=1
                    if self.update:
                        print("camera1: ",self.eyeposcam1)
                        print("camera2: ",self.eyeposcam2)
                        print(f"==============================({self.sunpos1[0]}, {self.sunpos1[1]}, {self.sunpos2[0]},{self.sunpos2[1]} )==========================")
                        self.calculatedleft = eyePos3D.runEyePos3D(self.eyeposcam1[0][0],self.eyeposcam1[0][1],self.eyeposcam2[0][0],self.eyeposcam2[0][1])
                        self.calculatedright = eyePos3D.runEyePos3D(self.eyeposcam1[1][0],self.eyeposcam1[1][1],self.eyeposcam2[1][0],self.eyeposcam2[1][1])                
                        self.calculatedsun = sunPos3D_new.runSunPos3D(self.sunpos1[0],self.sunpos1[1],self.sunpos2[0],self.sunpos2[1])
                        self.calculateddp = display_new.caldisplay(self.calculatedleft,self.calculatedright,self.calculatedsun)
                        self.message = [1,int(self.calculateddp[0]),int(self.calculateddp[1])]
                        if  (0 <= self.message[1] and self.message[1] <= 100) and (0 <= self.message[2] and self.message[2] <= 100):
                            await websocket.send(f"({self.message[0]},{self.message[2]},{self.message[1]})")
                            print(f"({self.message[0]},{self.message[2]},{self.message[1]})sended")
                        self.update = False
                    #end of while
                    if self.num == 2:
                        self.num = 3
                    else:
                        self.num = 2
                    cnt+=1
                    picam0.close()
                    try:
                        picam0.close()
                    except:
                        pass
                #end of while
                self.num=0
                self.update = False
                try:
                    picam0.close()
                except:
                    pass
            
    def set_sun_center(self,center):
        self.sun_center = [int(center[0]), int(center[1])]
    def get_sun_center(self):
        return self.sun_center
    def mod_sun_center(self,image):
        self.sun_center = [self.sun_center[0]- (image.shape[1] / 2), self.sun_center[1]- (image.shape[0] / 2)]
        self.sun_center[1] = self.sun_center[1] * -1
        return 
        
server1 =server([0,0,0],False)
