import numpy as np
from app.thermal.capture import ThermalCapture

class ThermalMotorController:
    def __init__(self, angle_per_col=5.625):
        self.center_col = 16  # 0~31, 중앙
        self.min_angle = -90
        self.max_angle = 90
        self.angle_per_col = angle_per_col  # 180도/32픽셀
        self.current_angle = 0  # 시작은 정면(0°)
        self.capture = ThermalCapture()

    def get_thermal_and_decide(self):
        arr = np.array(self.capture.get_data())
        max_row, max_col = np.unravel_index(np.argmax(arr), arr.shape)

        # 목표 각도 계산
        target_angle = (max_col - self.center_col) * self.angle_per_col

        # 이동 각도 제한
        target_angle = min(max(target_angle, self.min_angle), self.max_angle)

        # 이동해야 할 각도 차이 계산 (현재 위치 기준)
        move_angle = target_angle - self.current_angle

        if abs(move_angle) < 1:  # 1° 미만이면 이동 안 함(임계값)
            direction = "none"
            move_angle = 0
        elif move_angle > 0:
            direction = "right"
        else:
            direction = "left"

        # 모터 이동(직접 하드웨어와 연결 필요)
        if direction != "none":
            self.move_motor(direction, abs(move_angle))
            self.current_angle = target_angle  # 위치 갱신

        return {
            "direction": direction,
            "move_angle": abs(move_angle),
            "current_angle": self.current_angle,
            "max_col": max_col,
            "max_temp": arr[max_row, max_col]
        }

    def move_motor(self, direction, angle):
        # TODO: 각도(angle)에 맞게 스텝모터 또는 서보모터 제어
        print(f"모터 {direction}로 {angle:.2f}도 이동")

# 사용 예시
if __name__ == "__main__":
    controller = ThermalMotorController()
    while True:
        result = controller.get_thermal_and_decide()
        print(result)
        import time
        time.sleep(1)
