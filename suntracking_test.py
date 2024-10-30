import cv2
import numpy as np
from picamera2 import Picamera2, Preview
import sunPos3D

# 실시간 태양 추적 함수
def sun_tracking_from_camera():
    picam2 = Picamera2(2)  # Picamera2 객체 생성
    config = picam2.create_preview_configuration(main={"size": (640, 480)})  # 미리보기 설정
    picam2.configure(config)
    picam2.start()  # 카메라 미리보기 시작
    
    while True:
        frame = picam2.capture_array()  # Picamera2에서 이미지를 캡처
        print(frame.shape)

        # 이미지를 그레이스케일로 변환
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 그레이스케일 이미지에서 가장 밝은 부분 찾기
        #(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
        #sunpos=[maxLoc[0]- (frame.shape[1] / 2), maxLoc[1]- (frame.shape[0] / 2)]
        #반전
        #sunpos[0] = sunpos[0] * -1 
        #sunpos[1] = sunpos[1] * -1

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # BGR로 변환 (Picamera는 기본적으로 RGB를 반환)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred_image = cv2.GaussianBlur(gray, (51, 51), 0)
        _, threshold_img = cv2.threshold(blurred_image, 252, 255, cv2.THRESH_BINARY)
        moments = cv2.moments(threshold_img, True)
        if moments['m00'] != 0:  # Prevent division by zero
            center_x = int(moments['m10'] / moments['m00'])
            center_y = int(moments['m01'] / moments['m00'])
            sunpos = [center_x, center_y]
        
        # 태양의 위치에 원 그리기
        cv2.circle(frame, sunpos, 20, (0, 0, 255), 2)
        
        # 태양의 위치를 실시간으로 표시
        cv2.putText(frame, f"Sun Position: {sunpos}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # 결과 영상 출력
        cv2.imshow("Sun Tracking (Press 'q' to quit)", frame)
        
        # 'q' 키를 누르면 루프를 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 카메라 자원 해제
    picam2.close()
    cv2.destroyAllWindows()

# 실시간 태양 추적 실행
if __name__ == "__main__":
    sun_tracking_from_camera()
