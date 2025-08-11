from threading import Thread
from network.camera_sender import send_camera_stream
from network.thermal_sender import send_thermal_data

def run_all_senders():
    t1 = Thread(target=send_camera_stream, daemon=True)
    t2 = Thread(target=send_thermal_data, daemon=True)

    t1.start()
    t2.start()

    t1.join()
    t2.join()