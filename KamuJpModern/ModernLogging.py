import sys

class ModernLogging:
    def __init__(self, process_name):
        self.process_name = process_name

    def log(self, message, level="INFO"):
        if level == "INFO":
            print(f"{self.process_name} - {self._color(34)}INFO{self._color(0)} - {message}")
        elif level == "WARNING":
            print(f"{self.process_name} - {self._color(33)}WARNING{self._color(0)} - {message}")
        elif level == "ERROR":
            print(f"{self.process_name} - {self._color(31)}ERROR{self._color(0)} - {message}")
        else:
            print(f"{self.process_name} - {self._color(35)}DEBUG{self._color(0)} - {message}")

    def _color(self, color_code):
        return f"\033[{color_code}m"