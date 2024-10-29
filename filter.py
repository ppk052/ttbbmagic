from filterpy.kalman import KalmanFilter
import numpy as np

# Kalman Filter 설정
kf = KalmanFilter(dim_x=3, dim_z=3)
kf.x = np.array([[0.], [0.], [0.]])  # 초기 상태
kf.F = np.eye(3)  # 상태 전이 행렬 (identity matrix)
kf.H = np.eye(3)  # 관측 모델 행렬
kf.P *= 1000.0    # 초기 불확실성 (high uncertainty)
kf.R = np.eye(3) * 5  # 측정 노이즈 행렬
kf.Q = np.eye(3) * 0.1  # 프로세스 노이즈 행렬 (필요에 따라 조정)

#저주파필터
alpha = 0.5
previous_position = None
def kalmanfilter(data):
    kf.predict()
    kf.update(data)
    return kf.x.flatten()

def lowpassfilter(data):
    if previous_position is None:
        previous_position = data
    else:
        previous_position = (alpha*data+(1-alpha)*previous_position)
    return previous_position