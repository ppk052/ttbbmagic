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
                    x = int(face_landmarks.landmark[idx].x * image.shape[1]) - (image.shape[1] / 2)
                    y = int(face_landmarks.landmark[idx].y * image.shape[0]) - (image.shape[0] / 2)
                    left_iris_points.append((x, y))
                left_iris_points = np.array(left_iris_points, dtype=np.int32)
                (lx, ly), left_radius = cv2.minEnclosingCircle(left_iris_points)
                left_center = (int(lx) * -1, int(ly) * -1)
                left_radius = int(left_radius)
                cv2.circle(image, left_center, left_radius, (0, 255, 0), 1)

                left_iris_text = f"Left pupil: ({left_center[0]}, {left_center[1]})"
                cv2.putText(image, left_iris_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)

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
                cv2.circle(image, right_center, right_radius, (0, 255, 0), 1)

                right_iris_text = f"Right pupil: ({right_center[0]}, {right_center[1]})"
                cv2.putText(image, right_iris_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)

        # 결과 이미지 표시
        cv2.imshow('MediaPipe Iris', image)
        if cv2.waitKey(5) & 0xFF == 27:  # Esc 키로 종료
            break

cv2.destroyAllWindows()
picam2.close()
