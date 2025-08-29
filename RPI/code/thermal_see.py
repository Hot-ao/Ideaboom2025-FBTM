import board
import busio
import numpy as np
import adafruit_mlx90640
import matplotlib.pyplot as plt
import time

# I2C ����
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_4_HZ

frame = np.zeros((24*32))

plt.ion()  # ���ͷ�Ƽ�� ��� �ѱ�
fig, ax = plt.subplots()
thermal_img = ax.imshow(np.zeros((24,32)), cmap='inferno', vmin=20, vmax=40)
fig.colorbar(thermal_img, ax=ax)
plt.title("Real-time MLX90640 Thermal Visualization")

while True:
    try:
        mlx.getFrame(frame)
        data_array = np.reshape(frame, (24, 32))

        # ���� ���� - ����ó�� ���ϴ� ���� �߰������� ���� ����
        error_array = data_array[22:24, 12:14]
        data_array[23, 13] = np.median(error_array)

        thermal_img.set_data(data_array)
        thermal_img.set_clim(vmin=np.min(data_array), vmax=np.max(data_array))
        plt.draw()
        plt.pause(0.1)

    except RuntimeError:
        # Too many retries ���� �߻� �� �����ϰ� ��õ�
        continue
    except Exception as e:
        print("Error:", e)
        time.sleep(1)
