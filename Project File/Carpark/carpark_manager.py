# carpark_manager.py replaces the mocks.py
import time
from interfaces import CarparkDataProvider, CarparkSensorListener
# We import CarParkDisplay for type hinting, to tell Python what kind of object it expects
from CarParkDisplay import CarParkDisplay # Type hint

class CarparkManager(CarparkDataProvider, CarparkSensorListener):
    """
    This class is the 'brain' of the car park system.
    It keeps track of available spaces, temperature, and notifies the display
    when things change. It also listens for sensor events (cars, temperature).
    """
    def __init__(self, total_capacity: int = 100):
        self._total_capacity = total_capacity # Maximum cars the car park can hold
        self._current_available_spaces = total_capacity # How many spaces are currently free
        self._current_temperature = 20.0 # Initial temperature
        self._connected_display: CarParkDisplay | None = None # Reference to the display to update

    # --- Methods to PROVIDE data (for the display) ---
    @property
    def available_spaces(self) -> int:
        """Returns the number of parking spaces currently free."""
        return self._current_available_spaces

    @property
    def temperature(self) -> float:
        """Returns the current temperature recorded in the car park."""
        return self._current_temperature

    @property
    def current_time(self) -> time.struct_time:
        """Returns the current local time."""
        # This will use the computer's current local time.
        return time.localtime()

    # --- Methods to LISTEN for sensor events (from the detector) ---
    def incoming_car(self, license_plate: str):
        """Called when a sensor detects a car entering."""
        if self._current_available_spaces > 0:
            self._current_available_spaces -= 1 # One less space available
            print(f"[{time.strftime('%H:%M:%S', self.current_time)}] IN: {license_plate}. Spaces: {self._current_available_spaces}")
        else:
            print(f"[{time.strftime('%H:%M:%S', self.current_time)}] IN: {license_plate}. Car park is FULL!")
        self._notify_connected_display() # Tell the display to update its view

    def outgoing_car(self, license_plate: str):
        """Called when a sensor detects a car leaving."""
        if self._current_available_spaces < self._total_capacity:
            self._current_available_spaces += 1 # One more space available
            print(f"[{time.strftime('%H:%M:%S', self.current_time)}] OUT: {license_plate}. Spaces: {self._current_available_spaces}")
        else:
            print(f"[{time.strftime('%H:%M:%S', self.current_time)}] OUT: {license_plate}. Car park already EMPTY!")
        self._notify_connected_display() # Tell the display to update its view

    def temperature_reading(self, temperature: float):
        """Called when a temperature sensor provides a new reading."""
        self._current_temperature = temperature # Update the internal temperature
        print(f"[{time.strftime('%H:%M:%S', self.current_time)}] Temp update: {self._current_temperature}°C")
        self._notify_connected_display() # Tell the display to update its view

    # --- Method to connect with the display ---
    def set_display_to_update(self, display_object: 'CarParkDisplay'):
        """
        Connects this manager to a display, so it can tell the display to update.

        Args:
            display_object (CarParkDisplay): The CarParkDisplay instance to notify.
        """
        if isinstance(display_object, CarParkDisplay):
            self._connected_display = display_object
        else:
            raise TypeError("The object provided is not a CarParkDisplay instance.")

    def _notify_connected_display(self):
        """
        Internal method: Tells the connected display to get the latest data and refresh.
        """
        if self._connected_display:
            self._connected_display.refresh_display()