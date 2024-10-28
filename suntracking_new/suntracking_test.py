import cv2
import numpy as np
from picamera2 import Picamera2, Preview
import sundetector as sd

# 실시간 태양 추적 함수
def sun_tracking_from_camera():
    sundetector = sd.SunDetector()
    picam2 = Picamera2(2)  # Picamera2 객체 생성
    config = picam2.create_preview_configuration(main={"size": (640, 480)})  # 미리보기 설정
    picam2.configure(config)
    picam2.start()  # 카메라 미리보기 시작
    
    
    while True:
        frame = picam2.capture_array()  # Picamera2에서 이미지를 캡처
        print(frame.shape)

        # 이미지에서 태양 출력
        sundetector.set_frame(frame)
        sundetector.find_sun()
        sundetector.display("suntracking")
        
        # 'q' 키를 누르면 루프를 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 카메라 자원 해제
    picam2.close()
    cv2.destroyAllWindows()

# 실시간 태양 추적 실행
if __name__ == "__main__":
    sun_tracking_from_camera()
