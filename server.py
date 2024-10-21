from picamera2 import Picamera2, Preview
import websockets
import asyncio
import time
import eyePos3D
import sunPos3D
import mediapipe as mp
import numpy as np
import cv2
import os

class server:
    connected = False
    def __init__(self,message,status):
        self.eyeposcam1 = [[0,0],[0,0]]
        self.eyeposcam2 = [[0,0],[0,0]]
        self.sunpos = [0,0]
        self.num = 0
        self.update = False
        self.bright = 0;
        self.message = message  
        self.status = False    
        self.calculatedleft = [0,0,0]
        self.calculatedright = [0,0,0]
        self.message = message  
        self.status = False  
        start_server = websockets.serve(self.hello, "localhost", 8000)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever() 

    async def hello(self,websocket, path):
        os.system("chromium-browser --kiosk /home/pi/ttbbmagic/index.html")
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
            
            # Picamera2 초기화
            picam0=Picamera2(self.num)
            picam0.start()
            # Picamera2에서 이미지를 캡처
            image = picam0.capture_array()  
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # BGR로 변환 (Picamera는 기본적으로 RGB를 반환)
            print(f"{self.num}번째 카메라")
            # 0,1 : 동공좌표추출, 2:해좌표추출
            if self.num==0 or self.num == 1:
                with mp_face_mesh.FaceMesh(
                    max_num_faces=1,
                    refine_landmarks=True,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as face_mesh:
                    
                    # MediaPipe Face Mesh 처리
                    #results는 눈 잡았는지 확인하는 boolean
                    results = face_mesh.process(image)
                    if results.multi_face_landmarks:
                        for face_landmarks in results.multi_face_landmarks:
                            
                            # 왼쪽 홍채
                            left_iris_points = []
                            for idx in LEFT_IRIS:
                                x = int(face_landmarks.landmark[idx].x * image.shape[1])
                                y = int(face_landmarks.landmark[idx].y * image.shape[0])
                                left_iris_points.append((x, y))
                            left_iris_points = np.array(left_iris_points, dtype=np.int32)
                            (lx, ly), left_radius = cv2.minEnclosingCircle(left_iris_points)
                            left_center = (int(lx), int(ly))
                            left_radius = int(left_radius)
                            
                            # 오른쪽 홍채
                            right_iris_points = []
                            for idx in RIGHT_IRIS:
                                x = int(face_landmarks.landmark[idx].x * image.shape[1])
                                y = int(face_landmarks.landmark[idx].y * image.shape[0])
                                right_iris_points.append((x, y))
                            right_iris_points = np.array(right_iris_points, dtype=np.int32)
                            (rx, ry), right_radius = cv2.minEnclosingCircle(right_iris_points)
                            right_center = (int(rx), int(ry))
                            right_radius = int(right_radius)
                            if self.num==0:
                                self.eyeposcam1 = [[left_center[0],left_center[1]],[right_center[0],right_center[1]]]
                                print(self.eyeposcam1)
                            else:
                                self.eyeposcam2 = [[left_center[0],left_center[1]],[right_center[0],right_center[1]]]
                                print(self.eyeposcam2)
                            self.num += 1
            #태양위치추출
            if self.num==2:
                self.bright = np.mean(image)
                print(self.bright)
                #평균밝기가 일정 수치 이하일때 실행
                if self.bright <= 10:
                    try:
                        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(image)
                        self.sunpos=[maxLoc[0],maxLoc[1]]
                        self.update = True
                    except Exception as e:
                        print(e)
                        print("다음카메라로 넘어갑니다")
                        pass
                    # 태양의 위치에 원 그리기
                    #cv2.circle(image, maxLoc, 40, (0, 0, 255), 2)
                    self.num=0
            picam0.close()
            time.sleep(1)
            if self.update:
                #여기에 알고리즘계산하기
                self.calculatedleft = eyePos3D.runEyePos3D(self.eyeposcam1[0][0],self.eyeposcam1[0][1],self.eyeposcam2[0][0],self.eyeposcam2[0][1])
                self.calculatedright = eyePos3D.runEyePos3D(self.eyeposcam1[1][0],self.eyeposcam1[1][1],self.eyeposcam2[1][0],self.eyeposcam2[1][1])                
                self.message = [1,self.calculatedleft[0],self.calculatedleft[1]]
                await websocket.send(f"({self.message[0]},{self.message[1]},{self.message[2]})")
                print(f"({self.message[0]},{self.message[1]},{self.message[2]})sended")
                self.update = False
server1 =server([0,0,0],False)