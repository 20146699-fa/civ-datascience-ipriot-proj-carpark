import threading
import time
import tkinter as tk
from interfaces import CarparkDataProvider
from typing import Iterable

class WindowedDisplay:
    DISPLAY_INIT = '– – –'
    SEP = ':'

    def __init__(self, root, title: str, display_fields: Iterable[str]):
        self.window = tk.Toplevel(root)
        self.window.title(f'{title}: Parking')
        self.window.geometry('800x400')
        self.window.resizable(False, False)
        self.display_fields = display_fields

        self.gui_elements = {}
        for i, field in enumerate(self.display_fields):
            self.gui_elements[f'lbl_field_{i}'] = tk.Label(
                self.window, text=field + self.SEP, font=('Arial', 50))
            self.gui_elements[f'lbl_value_{i}'] = tk.Label(
                self.window, text=self.DISPLAY_INIT, font=('Arial', 50))
            self.gui_elements[f'lbl_field_{i}'].grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            self.gui_elements[f'lbl_value_{i}'].grid(row=i, column=2, sticky=tk.W, padx=10)

    def show(self):
        self.window.update()

    def update(self, updated_values: dict):
        for field in self.gui_elements:
            if field.startswith('lbl_field'):
                field_value = field.replace('field', 'value')
                label_key = self.gui_elements[field].cget('text').rstrip(self.SEP)
                self.gui_elements[field_value].configure(text=updated_values[label_key])
        self.window.update()

class CarParkDisplay:
    fields = ['Available bays', 'Temperature', 'At']

    def __init__(self, root):
        self.window = WindowedDisplay(root, 'Moondalup', CarParkDisplay.fields)
        self._provider = None
        updater = threading.Thread(target=self.check_updates)
        updater.daemon = True
        updater.start()
        self.window.show()

    @property
    def data_provider(self):
        return self._provider

    @data_provider.setter
    def data_provider(self, provider):
        if isinstance(provider, CarparkDataProvider):
            self._provider = provider

    def update_display(self):
        field_values = dict(zip(CarParkDisplay.fields, [
            f'{self._provider.available_spaces:03d}',
            f'{self._provider.temperature:02d}℃',
            time.strftime("%H:%M:%S", self._provider.current_time)
        ]))
        self.window.update(field_values)

    def check_updates(self):
        while True:
            time.sleep(1)
            if self._provider is not None:
                self.update_display()
