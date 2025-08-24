import numpy as np
from app.thermal.capture import ThermalCapture

class ThermalMotorController:
    def __init__(self, angle_per_col=5.625):
        self.center_col = 16  # Center column index of thermal data (0 to 31)
        self.min_angle = -90  # Min rotation limit (degrees)
        self.max_angle = 90   # Max rotation limit (degrees)
        self.angle_per_col = angle_per_col  # Rotation angle per column (180 degrees / 32 columns)
        self.current_angle = 0  # Current rotational angle of the motor
        self.current_side_pos = 0  # Current position of side motor (arbitrary units)
        self.capture = ThermalCapture()

    def get_thermal_and_decide(self):
        arr = np.array(self.capture.get_data())
        max_row, max_col = np.unravel_index(np.argmax(arr), arr.shape)

        # Calculate rotation target angle
        target_angle = (max_col - self.center_col) * self.angle_per_col
        target_angle = min(max(target_angle, self.min_angle), self.max_angle)
        move_angle = target_angle - self.current_angle

        if abs(move_angle) < 1:
            direction = "none"
            move_angle = 0
        elif move_angle > 0:
            direction = "right"
        else:
            direction = "left"

        if direction != "none":
            self.move_motor(direction, abs(move_angle))
            self.current_angle = target_angle

        # Additional logic for side movement motor (example: based on max_col)
        # Define side movement range e.g. from -10 to +10 units
        side_move_limit = 10  
        target_side_pos = (max_col - self.center_col) / self.center_col * side_move_limit
        side_move_dist = target_side_pos - self.current_side_pos

        if abs(side_move_dist) > 0.5:  # Threshold to reduce jitter
            if side_move_dist > 0:
                side_direction = "right"
            else:
                side_direction = "left"
            self.move_side_motor(side_direction, abs(side_move_dist))
            self.current_side_pos = target_side_pos
        else:
            side_direction = "none"
            side_move_dist = 0

        return {
            "rotation": {
                "direction": direction,
                "move_angle": abs(move_angle),
                "current_angle": self.current_angle,
            },
            "side_move": {
                "direction": side_direction,
                "distance": abs(side_move_dist),
                "current_pos": self.current_side_pos,
            },
            "max_col": max_col,
            "max_temp": arr[max_row, max_col]
        }

    def move_motor(self, direction, angle):
        # TODO: Implement rotation motor control (via GPIO or motor driver pins)
        print(f"Rotate motor {direction} by {angle:.2f} degrees")

    def move_side_motor(self, direction, distance):
        # TODO: Implement side movement motor control (e.g. linear actuation)
        print(f"Move side motor {direction} by {distance:.2f} units")

if __name__ == "__main__":
    controller = ThermalMotorController()
    import time
    while True:
        result = controller.get_thermal_and_decide()
        print(result)
        time.sleep(1)
