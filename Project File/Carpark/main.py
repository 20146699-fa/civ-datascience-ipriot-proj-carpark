import tkinter as tk
from CarParkDisplay import CarParkDisplay
from CarDetector import CarDetectorWindow
from carpark_manager import CarparkManager  # Replace with actual MQTT class

if __name__ == '__main__':
    root = tk.Tk()

    carpark_manager = CarparkManager()  # Implements CarparkDataProvider & CarparkSensorListener

    display = CarParkDisplay(root)
    display.data_provider = carpark_manager

    detector = CarDetectorWindow(root)
    detector.add_listener(carpark_manager)

    root.mainloop()

