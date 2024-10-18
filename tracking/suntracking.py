import cv2
import numpy as np

# 실시간 태양 추적 함수
def sun_tracking_from_camera():
    cap = cv2.VideoCapture(0)  # 웹캠 연결 (0은 기본 카메라 장치)
    
    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return
    
    while True:
        ret, frame = cap.read()  # 프레임 읽기
        if not ret:
            print("프레임을 가져올 수 없습니다.")
            break

        # 이미지를 그레이스케일로 변환
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 그레이스케일 이미지에서 가장 밝은 부분 찾기
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
        
        # 태양의 위치에 원 그리기
        cv2.circle(frame, maxLoc, 40, (0, 0, 255), 2)
        
        # 태양의 위치를 실시간으로 표시
        cv2.putText(frame, f"Sun Position: {maxLoc}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        # 결과 영상 출력
        cv2.imshow("Sun Tracking (Press 'q' to quit)", frame)
        
        # 'q' 키를 누르면 루프를 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 카메라 자원 해제
    cap.release()
    cv2.destroyAllWindows()

# 실시간 태양 추적 실행
sun_tracking_from_camera()
