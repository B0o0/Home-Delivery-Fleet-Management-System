import threading
import time
from .map_socket import sio
#Function that runs the driver on a randomly generated route, driver moves until an order is given.
class Driver_Thread(threading.Thread):

    def __init__(self, route, driver_number, step_time):
        super().__init__()
        self.stop_event = threading.Event()
        self.route = route
        self.step_time = step_time
        self.driver_number = driver_number

    def run(self):
        try:
            for j in range(1, len(self.route)-1):  
                driver_num = str(self.driver_number) 
                location = self.route[j + 1]
                sio.emit("UpdateActiveDriverLocation", {driver_num:location})
                print("Driver location updated successfully")
                time.sleep(self.step_time)
                if self.stop_event.is_set():
                    break

        except AttributeError:
            pass

    def stop(self):
        self.stop_event.set()

