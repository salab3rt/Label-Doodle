import keyboard
from PyQt6.QtCore import QObject, pyqtSignal
import time

class HotkeyManager(QObject):
    ctrlPressedTwice = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.ctrl_pressed_count = 0
        self.last_ctrl_press_time = 0
        self.ctrl_pressed = False
        keyboard.on_press_key('ctrl', self.on_ctrl_pressed)
        keyboard.on_release_key('ctrl', self.on_ctrl_released)

    def on_ctrl_pressed(self, event):
        current_time = time.time()
        if not self.ctrl_pressed:
            self.ctrl_pressed = True
            if current_time - self.last_ctrl_press_time < 0.5:
                self.ctrl_pressed_count += 1
                if self.ctrl_pressed_count == 2:
                    self.ctrlPressedTwice.emit()
                    self.ctrl_pressed_count = 0
            else:
                self.ctrl_pressed_count = 1
            self.last_ctrl_press_time = current_time

    def on_ctrl_released(self, event):
        self.ctrl_pressed = False
