import board
import busio
import numpy as np
import adafruit_mlx90640
import time
import requests

SERVER_URL = 'http://192.168.0.162:5000/thermal/upload_endpoint' #MECA
#SERVER_URL = 'http://192.168.200.171:5000/thermal/upload_endpoint' #HOME
#SERVER_URL = 'http://fbtm761.duckdns.org:5000/thermal/upload_endpoint' #DUCKDNS

# I2C setup
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_4_HZ

frame = np.zeros((24*32))  # 768 values for one frame

while True:
    try:
        mlx.getFrame(frame)  # Read data from MLX90640
        data_array = np.reshape(frame, (24,32))  # Reshape to 24x32 array
        
        # Change error_data
        error_array = data_array[22:24,12:14]
        data_array[23,13]=np.median(error_array)
        
        payload = {'data':data_array.tolist()}
        requests.post(SERVER_URL, json=payload)
        time.sleep(0.1)
        
    except Exception as e:
        print("Error occurred:", e)
        time.sleep(1)