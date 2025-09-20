#/app/thermal/capture.py
import board
import busio
import numpy as np
import adafruit_mlx90640
import time

class ThermalCapture:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)

        while True:
            try:
                self.mlx = adafruit_mlx90640.MLX90640(i2c)
                self.mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_4_HZ
                break
            except RuntimeError as e:
                print(f"? MLX90640 init failed: {e}, retrying in 2s")
                time.sleep(2)

        self.frame = np.zeros((24*32))
    
    def get_data(self):
        while True:
            try:
                self.mlx.getFrame(self.frame)
                data_array = np.reshape(self.frame, (24, 32))
                error_array = data_array[22:24, 12:14]
                data_array[23, 13] = np.median(error_array)
                return data_array.tolist()
            except RuntimeError:
                time.sleep(0.05)