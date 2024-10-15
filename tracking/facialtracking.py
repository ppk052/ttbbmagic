'''
import cv2  # OpenCV 라이브러리를 가져옵니다.
import mediapipe as mp  # MediaPipe 라이브러리를 가져옵니다.
import numpy as np  # NumPy 라이브러리를 가져옵니다.

# Mediapipe 솔루션 초기화
mp_face_mesh = mp.solutions.face_mesh  # 얼굴 메쉬(landmark) 검출을 위한 MediaPipe Face Mesh 솔루션을 초기화합니다.
mp_drawing = mp.solutions.drawing_utils  # MediaPipe에서 제공하는 그리기 유틸리티를 초기화합니다.

# 홍채의 랜드마크 인덱스
LEFT_IRIS = [474, 475, 476, 477]  # 왼쪽 홍채를 구성하는 랜드마크 인덱스를 정의합니다.
#LEFT_IRIS = [1, 2, 98, 327] #코&코주위 랜드마크
RIGHT_IRIS = [469, 470, 471, 472]  # 오른쪽 홍채를 구성하는 랜드마크 인덱스를 정의합니다.

# 웹캠 캡처 초기화
cap = cv2.VideoCapture(0)  # 기본 웹캠을 사용하여 비디오 캡처 객체를 초기화합니다.

with mp_face_mesh.FaceMesh(
    max_num_faces=1,  # 최대 감지할 얼굴 수를 1로 설정합니다.
    refine_landmarks=True,  # 홍채 추적을 위해 랜드마크 정제를 활성화합니다.
    min_detection_confidence=0.5,  # 얼굴 검출에 대한 최소 신뢰도 임계값을 설정합니다.
    min_tracking_confidence=0.5) as face_mesh:  # 얼굴 추적에 대한 최소 신뢰도 임계값을 설정합니다.

    while cap.isOpened():  # 캡처가 열려 있는 동안 루프를 실행합니다.
        success, image = cap.read()  # 웹캠에서 프레임을 읽어옵니다.
        if not success:  # 프레임 읽기에 실패하면 메시지를 출력하고 루프를 종료합니다.
            print("카메라에서 영상을 가져올 수 없습니다.")
            break

        # 성능 향상을 위해 이미지 작성을 선택적으로 불변으로 설정
        image.flags.writeable = False  # 이미지를 불변으로 설정하여 성능을 향상시킵니다.
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # BGR 이미지를 RGB로 변환합니다.
        results = face_mesh.process(image)  # MediaPipe Face Mesh를 사용하여 이미지를 처리합니다.

        # 이미지 작성을 다시 설정
        image.flags.writeable = True  # 이미지를 다시 쓸 수 있게 설정합니다.
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # RGB 이미지를 BGR로 변환합니다.

        if results.multi_face_landmarks:  # 얼굴 랜드마크가 검출된 경우
            for face_landmarks in results.multi_face_landmarks:  # 검출된 각 얼굴에 대해
                # 왼쪽 홍채 랜드마크 그리기
                left_iris_points = []  # 왼쪽 홍채 랜드마크 좌표를 저장할 리스트를 초기화합니다.
                for idx in LEFT_IRIS:  # 왼쪽 홍채의 각 랜드마크 인덱스에 대해
                    x = int(face_landmarks.landmark[idx].x * image.shape[1])  # x 좌표를 이미지 크기에 맞게 변환합니다.
                    y = int(face_landmarks.landmark[idx].y * image.shape[0])  # y 좌표를 이미지 크기에 맞게 변환합니다.
                    left_iris_points.append((x, y))  # 변환된 좌표를 리스트에 추가합니다.
                left_iris_points = np.array(left_iris_points, dtype=np.int32)  # 좌표 리스트를 NumPy 배열로 변환합니다.
                (lx, ly), left_radius = cv2.minEnclosingCircle(left_iris_points)  # 최소 외접원을 계산하여 중심과 반지름을 얻습니다.
                left_center = (int(lx), int(ly))  # 중심 좌표를 정수로 변환합니다.
                left_radius = int(left_radius)  # 반지름을 정수로 변환합니다.
                cv2.circle(image, left_center, left_radius, (0, 255, 0), 1)  # 왼쪽 홍채를 원으로 그립니다.
                
                # 왼쪽 홍채 중심 좌표 텍스트 표시
                left_iris_text = f"Left pupil: ({left_center[0]}, {left_center[1]})"  # 왼쪽 홍채 중심 좌표 텍스트를 생성합니다.
                cv2.putText(image, left_iris_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)  # 이미지에 텍스트를 표시합니다.

                # 오른쪽 홍채 랜드마크 그리기
                right_iris_points = []  # 오른쪽 홍채 랜드마크 좌표를 저장할 리스트를 초기화합니다.
                for idx in RIGHT_IRIS:  # 오른쪽 홍채의 각 랜드마크 인덱스에 대해
                    x = int(face_landmarks.landmark[idx].x * image.shape[1])  # x 좌표를 이미지 크기에 맞게 변환합니다.
                    y = int(face_landmarks.landmark[idx].y * image.shape[0])  # y 좌표를 이미지 크기에 맞게 변환합니다.
                    right_iris_points.append((x, y))  # 변환된 좌표를 리스트에 추가합니다.
                right_iris_points = np.array(right_iris_points, dtype=np.int32)  # 좌표 리스트를 NumPy 배열로 변환합니다.
                (rx, ry), right_radius = cv2.minEnclosingCircle(right_iris_points)  # 최소 외접원을 계산하여 중심과 반지름을 얻습니다.
                right_center = (int(rx), int(ry))  # 중심 좌표를 정수로 변환합니다.
                right_radius = int(right_radius)  # 반지름을 정수로 변환합니다.
                cv2.circle(image, right_center, right_radius, (0, 255, 0), 1)  # 오른쪽 홍채를 원으로 그립니다.
                
                # 오른쪽 홍채 중심 좌표 텍스트 표시
                right_iris_text = f"Right pupil: ({right_center[0]}, {right_center[1]})"  # 오른쪽 홍채 중심 좌표 텍스트를 생성합니다.
                cv2.putText(image, right_iris_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)  # 이미지에 텍스트를 표시합니다.

        # 결과 이미지 표시
        cv2.imshow('MediaPipe Iris', image)  # 결과 이미지를 화면에 표시합니다.
        if cv2.waitKey(5) & 0xFF == 27:  # 사용자가 'Esc' 키를 누르면 루프를 종료합니다.
            break

cap.release()  # 웹캠 캡처를 해제합니다.
cv2.destroyAllWindows()  # 모든 OpenCV 윈도우를 닫습니다.
'''

from picamera2 import Picamera2, Preview
import mediapipe as mp
import numpy as np
import cv2

# Mediapipe 솔루션 초기화
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# 홍채의 랜드마크 인덱스
LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]

# Picamera2 초기화
picam2 = Picamera2()  # Picamera2 객체 생성
config = picam2.create_preview_configuration(main={"size": (640, 480)})  # 미리보기 설정
picam2.configure(config)
picam2.start()  # 카메라 미리보기 시작

with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:

    while True:
        image = picam2.capture_array()  # Picamera2에서 이미지를 캡처
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # BGR로 변환 (Picamera는 기본적으로 RGB를 반환)

        # MediaPipe Face Mesh 처리
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
                cv2.circle(image, left_center, left_radius, (0, 255, 0), 1)

                left_iris_text = f"Left pupil: ({left_center[0]}, {left_center[1]})"
                cv2.putText(image, left_iris_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)

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
                cv2.circle(image, right_center, right_radius, (0, 255, 0), 1)

                right_iris_text = f"Right pupil: ({right_center[0]}, {right_center[1]})"
                cv2.putText(image, right_iris_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)

        # 결과 이미지 표시
        cv2.imshow('MediaPipe Iris', image)
        if cv2.waitKey(5) & 0xFF == 27:  # Esc 키로 종료
            break

cv2.destroyAllWindows()
picam2.close()
